from yowsup.layers import YowProtocolLayer
from yowsup.layers.axolotl.protocolentities import *
from yowsup.layers.network.layer import YowNetworkLayer
from yowsup.layers import EventCallback
from yowsup.profile.profile import YowProfile

from yowsup.axolotl import exceptions
from yowsup.layers.axolotl.props import PROP_IDENTITY_AUTOTRUST

import logging
logger = logging.getLogger(__name__)


class AxolotlBaseLayer(YowProtocolLayer):
    def __init__(self):
        super(AxolotlBaseLayer, self).__init__()
        self._manager = None  # type: AxolotlManager | None
        self.skipEncJids = []

    def send(self, node):
        pass

    def receive(self, node):
        self.processIqRegistry(node)

    @property
    def manager(self):
        """
        :return:
        :rtype: AxolotlManager
        """
        return self._manager

    @EventCallback(YowNetworkLayer.EVENT_STATE_CONNECTED)
    def on_connected(self, yowLayerEvent):
        profile = self.getProp("profile")  # type: YowProfile
        self._manager = profile.axolotl_manager

    @EventCallback(YowNetworkLayer.EVENT_STATE_DISCONNECTED)
    def on_disconnected(self, yowLayerEvent):
        self._manager = None

    def getKeysFor(self, jids, resultClbk, errorClbk = None, reason=None):
        logger.debug("getKeysFor(jids=%s, resultClbk=[omitted], errorClbk=[omitted], reason=%s)" % (jids, reason))

        def onSuccess(resultNode, getKeysEntity):
            entity = ResultGetKeysIqProtocolEntity.fromProtocolTreeNode(resultNode)
            resultJids = entity.getJids()
            successJids = []
            errorJids = entity.getErrors() #jid -> exception

            for jid in getKeysEntity.jids:
                if jid not in resultJids:
                    self.skipEncJids.append(jid)
                    continue

                recipient_id = jid.split('@')[0]
                preKeyBundle = entity.getPreKeyBundleFor(jid)
                try:
                    self.manager.create_session(recipient_id, preKeyBundle,
                                                autotrust=self.getProp(PROP_IDENTITY_AUTOTRUST, False))
                    successJids.append(jid)
                except exceptions.UntrustedIdentityException as e:
                        errorJids[jid] = e
                        logger.error(e)
                        logger.warning("Ignoring message with untrusted identity")

            resultClbk(successJids, errorJids)

        def onError(errorNode, getKeysEntity):
            if errorClbk:
                errorClbk(errorNode, getKeysEntity)

        entity = GetKeysIqProtocolEntity(jids, reason=reason)
        self._sendIq(entity, onSuccess, onError=onError)
