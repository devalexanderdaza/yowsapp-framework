from axolotl.state.prekeystore import PreKeyStore
from axolotl.state.prekeyrecord import PreKeyRecord
from yowsup.axolotl.exceptions import InvalidKeyIdException
import sys


class LitePreKeyStore(PreKeyStore):
    def __init__(self, dbConn):
        """
        :type dbConn: Connection
        """
        self.dbConn = dbConn
        dbConn.execute("CREATE TABLE IF NOT EXISTS prekeys (_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "prekey_id INTEGER UNIQUE, sent_to_server BOOLEAN, record BLOB);")

    def loadPreKey(self, preKeyId):
        q = "SELECT record FROM prekeys WHERE prekey_id = ?"

        cursor = self.dbConn.cursor()
        cursor.execute(q, (preKeyId,))

        result = cursor.fetchone()
        if not result:
            raise InvalidKeyIdException("No such prekeyrecord!")

        return PreKeyRecord(serialized = result[0])

    def loadUnsentPendingPreKeys(self):
        q = "SELECT record FROM prekeys WHERE sent_to_server is NULL or sent_to_server = ?"

        cursor = self.dbConn.cursor()
        cursor.execute(q, (0,))

        result = cursor.fetchall()

        return [PreKeyRecord(serialized=result[0]) for result in result]

    def setAsSent(self, prekeyIds):
        """
        :param preKeyIds:
        :type preKeyIds: list
        :return:
        :rtype:
        """
        for prekeyId in prekeyIds:
            q = "UPDATE prekeys SET sent_to_server = ? WHERE prekey_id = ?"
            cursor = self.dbConn.cursor()
            cursor.execute(q, (1, prekeyId))
        self.dbConn.commit()

    def loadPendingPreKeys(self):
        q = "SELECT record FROM prekeys"
        cursor = self.dbConn.cursor()
        cursor.execute(q)
        result = cursor.fetchall()

        return [PreKeyRecord(serialized=result[0]) for result in result]

    def storePreKey(self, preKeyId, preKeyRecord):
        #self.removePreKey(preKeyId)
        q = "INSERT INTO prekeys (prekey_id, record) VALUES(?,?)"
        cursor = self.dbConn.cursor()
        serialized = preKeyRecord.serialize()
        cursor.execute(q, (preKeyId, buffer(serialized) if sys.version_info < (2,7) else serialized))
        self.dbConn.commit()

    def containsPreKey(self, preKeyId):
        q = "SELECT record FROM prekeys WHERE prekey_id = ?"
        cursor = self.dbConn.cursor()
        cursor.execute(q, (preKeyId,))
        return cursor.fetchone() is not None

    def removePreKey(self, preKeyId):
        q = "DELETE FROM prekeys WHERE prekey_id = ?"
        cursor = self.dbConn.cursor()
        cursor.execute(q, (preKeyId,))
        self.dbConn.commit()

    def loadMaxPreKeyId(self):
        q = "SELECT max(prekey_id) FROM prekeys"
        cursor = self.dbConn.cursor()
        cursor.execute(q)
        result = cursor.fetchone()
        return 0 if result[0] is None else result[0]
