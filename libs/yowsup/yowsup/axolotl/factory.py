from yowsup.axolotl.manager import AxolotlManager
from yowsup.common.tools import StorageTools
from yowsup.axolotl.store.sqlite.liteaxolotlstore import LiteAxolotlStore
import logging

logger = logging.getLogger(__name__)


class AxolotlManagerFactory(object):
    DB = "axolotl.db"

    def get_manager(self, profile_name, username):
        logger.debug("get_manager(profile_name=%s, username=%s)" % (profile_name, username))
        dbpath = StorageTools.constructPath(profile_name, self.DB)
        store = LiteAxolotlStore(dbpath)
        return AxolotlManager(store, username)
