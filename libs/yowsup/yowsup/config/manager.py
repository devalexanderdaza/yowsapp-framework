from yowsup.config.v1.config import Config
from yowsup.config.transforms.dict_keyval import DictKeyValTransform
from yowsup.config.transforms.dict_json import DictJsonTransform
from yowsup.config.v1.serialize import ConfigSerialize
from yowsup.common.tools import StorageTools
import logging
import os

logger = logging.getLogger(__name__)


class ConfigManager(object):
    NAME_FILE_CONFIG = "config"

    TYPE_KEYVAL = 1
    TYPE_JSON = 2

    TYPE_NAMES = {
        TYPE_KEYVAL: "keyval",
        TYPE_JSON: "json"
    }

    MAP_EXT = {
        "yo": TYPE_KEYVAL,
        "json": TYPE_JSON,
    }

    TYPES = {
        TYPE_KEYVAL: DictKeyValTransform,
        TYPE_JSON: DictJsonTransform
    }

    def load(self, path_or_profile_name, profile_only=False):
        # type: (str, bool) -> Config
        """
        Will first try to interpret path_or_profile_name as direct path to a config file and load from there. If
        this fails will interpret it as profile name and load from profile dir.
        :param path_or_profile_name:
        :param profile_only
        :return Config instance, or None if no config could be found
        """
        logger.debug("load(path_or_profile_name=%s, profile_only=%s)" % (path_or_profile_name, profile_only))

        exhausted = []
        if not profile_only:
            config = self._load_path(path_or_profile_name)
        else:
            config = None
        if config is not None:
            return config
        else:
            logger.debug("path_or_profile_name is not a path, using it as profile name")
            if not profile_only:
                exhausted.append(path_or_profile_name)
            profile_name = path_or_profile_name
            config_dir = StorageTools.getStorageForProfile(profile_name)
            logger.debug("Detecting config for profile=%s, dir=%s" % (profile_name, config_dir))
            for ftype in self.MAP_EXT:
                if len(ftype):
                    fname = (self.NAME_FILE_CONFIG + "." + ftype)
                else:
                    fname = self.NAME_FILE_CONFIG

                fpath = os.path.join(config_dir, fname)
                logger.debug("Trying %s" % fpath)
                if os.path.isfile(fpath):
                    return self._load_path(fpath)

                exhausted.append(fpath)

            logger.error("Could not find a config for profile=%s, paths checked: %s" % (profile_name, ":".join(exhausted)))

    def _type_to_str(self, type):
        """
        :param type:
        :type type: int
        :return:
        :rtype:
        """
        for key, val in self.TYPE_NAMES.items():
            if key == type:
                return val

    def _load_path(self, path):
        """
        :param path:
        :type path:
        :return:
        :rtype:
        """
        logger.debug("_load_path(path=%s)" % path)
        if os.path.isfile(path):
            configtype = self.guess_type(path)
            logger.debug("Detected config type: %s" % self._type_to_str(configtype))
            if configtype in self.TYPES:
                logger.debug("Opening config for reading")
                with open(path, 'r') as f:
                    data = f.read()
                datadict = self.TYPES[configtype]().reverse(data)
                return self.load_data(datadict)
            else:
                raise ValueError("Unsupported config type")
        else:
            logger.debug("_load_path couldn't find the path: %s" % path)

    def load_data(self, datadict):
        logger.debug("Loading config")
        return ConfigSerialize(Config).deserialize(datadict)

    def guess_type(self, config_path):
        dissected = os.path.splitext(config_path)
        if len(dissected) > 1:
            ext = dissected[1][1:].lower()
            config_type = self.MAP_EXT[ext] if ext in self.MAP_EXT else None
        else:
            config_type = None

        if config_type is not None:
            return config_type
        else:
            logger.debug("Trying auto detect config type by parsing")
            with open(config_path, 'r') as f:
                data = f.read()
            for config_type, transform in self.TYPES.items():
                config_type_str = self.TYPE_NAMES[config_type]
                try:
                    logger.debug("Trying to parse as %s" % config_type_str)
                    if transform().reverse(data):
                        logger.debug("Successfully detected %s as config type for %s" % (config_type_str, config_path))
                        return config_type
                except Exception as ex:
                    logger.debug("%s was not parseable as %s, reason: %s" % (config_path, config_type_str, ex))

    def get_str_transform(self, serialize_type):
        if serialize_type in self.TYPES:
            return self.TYPES[serialize_type]()

    def config_to_str(self, config, serialize_type=TYPE_JSON):
        transform = self.get_str_transform(serialize_type)
        if transform is not None:
            return transform.transform(ConfigSerialize(config.__class__).serialize(config))

        raise ValueError("unrecognized serialize_type=%d" % serialize_type)

    def save(self, profile_name, config, serialize_type=TYPE_JSON, dest=None):
        outputdata = self.config_to_str(config, serialize_type)
        if dest is None:
            StorageTools.writeProfileConfig(profile_name, outputdata)
        else:
            with open(dest, 'wb') as outputfile:
                outputfile.write(outputdata)
