import json
import os
import unittest

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))


def _load(name):
    with open(os.path.join(ROOT, "snapshots", name + ".json"), encoding="utf-8") as f:
        return json.load(f)


class V040OracleTests(unittest.TestCase):
    """Values double-checked against canonical jmcorgan/fips@v0.4.0 source (commit
    d5ee526f0e15d6e7a6336cf5746c763f4d1779e8). Upstream is authoritative; microfips
    is only a downstream cross-check."""

    def setUp(self):
        self.snap = _load("v0.4.0")

    def test_authoritative_source_is_canonical_jmcorgan(self):
        self.assertEqual(self.snap["upstream"]["authority"], "jmcorgan/fips")
        self.assertEqual(self.snap["upstream"]["ref"], "v0.4.0")
        self.assertTrue(self.snap["upstream"]["commit"].startswith("d5ee526"))

    def test_no_missing_expected(self):
        self.assertEqual(self.snap["missing_expected"]["consts"], [])
        self.assertEqual(self.snap["missing_expected"]["enums"], [])

    def test_noise_consts(self):
        c = self.snap["consts"]
        self.assertEqual(c["MAX_MESSAGE_SIZE"]["value"], 65535)
        self.assertEqual(c["TAG_SIZE"]["value"], 16)
        self.assertEqual(c["PUBKEY_SIZE"]["value"], 33)
        self.assertEqual(c["EPOCH_SIZE"]["value"], 8)
        self.assertEqual(c["EPOCH_ENCRYPTED_SIZE"]["value"], 24)
        self.assertEqual(c["HANDSHAKE_MSG1_SIZE"]["value"], 106)
        self.assertEqual(c["HANDSHAKE_MSG2_SIZE"]["value"], 57)
        self.assertEqual(c["XK_HANDSHAKE_MSG1_SIZE"]["value"], 33)
        self.assertEqual(c["XK_HANDSHAKE_MSG2_SIZE"]["value"], 57)
        self.assertEqual(c["XK_HANDSHAKE_MSG3_SIZE"]["value"], 73)
        self.assertEqual(c["REPLAY_WINDOW_SIZE"]["value"], 2048)

    def test_protocol_and_session_consts(self):
        c = self.snap["consts"]
        self.assertEqual(c["PROTOCOL_VERSION"]["value"], 1)
        self.assertEqual(c["SESSION_DATAGRAM_HEADER_SIZE"]["value"], 36)
        self.assertEqual(c["SESSION_SENDER_REPORT_SIZE"]["value"], 46)
        self.assertEqual(c["SESSION_RECEIVER_REPORT_SIZE"]["value"], 66)
        self.assertEqual(c["PATH_MTU_NOTIFICATION_SIZE"]["value"], 2)
        self.assertEqual(c["COORDS_REQUIRED_SIZE"]["value"], 34)
        self.assertEqual(c["MTU_EXCEEDED_SIZE"]["value"], 36)

    def test_mmp_report_sizes(self):
        c = self.snap["consts"]
        self.assertEqual(c["SENDER_REPORT_BODY_SIZE"]["value"], 47)
        self.assertEqual(c["RECEIVER_REPORT_BODY_SIZE"]["value"], 67)
        self.assertEqual(c["SENDER_REPORT_WIRE_SIZE"]["value"], 52)
        self.assertEqual(c["RECEIVER_REPORT_WIRE_SIZE"]["value"], 72)

    def test_link_message_type_enum(self):
        lm = self.snap["enums"]["LinkMessageType"]
        self.assertEqual(lm["SessionDatagram"], 0x00)
        self.assertEqual(lm["SenderReport"], 0x01)
        self.assertEqual(lm["ReceiverReport"], 0x02)
        self.assertEqual(lm["TreeAnnounce"], 0x10)
        self.assertEqual(lm["FilterAnnounce"], 0x20)
        self.assertEqual(lm["LookupRequest"], 0x30)
        self.assertEqual(lm["LookupResponse"], 0x31)
        self.assertEqual(lm["Disconnect"], 0x50)
        self.assertEqual(lm["Heartbeat"], 0x51)

    def test_disconnect_reason_enum(self):
        dr = self.snap["enums"]["DisconnectReason"]
        self.assertEqual(dr["Shutdown"], 0x00)
        self.assertEqual(dr["Restart"], 0x01)
        self.assertEqual(dr["ProtocolError"], 0x02)
        self.assertEqual(dr["TransportFailure"], 0x03)
        self.assertEqual(dr["ResourceExhaustion"], 0x04)
        self.assertEqual(dr["SecurityViolation"], 0x05)
        self.assertEqual(dr["ConfigurationChange"], 0x06)
        self.assertEqual(dr["Timeout"], 0x07)
        self.assertEqual(dr["Other"], 0xFF)


class MasterSnapshotTests(unittest.TestCase):
    """master is a moving target: tests assert structure and stable facts, not exact
    values. Drift vs v0.4.0 is captured in the snapshot's missing_expected field."""

    def setUp(self):
        self.snap = _load("master")

    def test_authoritative_source_is_canonical(self):
        self.assertEqual(self.snap["upstream"]["authority"], "jmcorgan/fips")
        self.assertEqual(self.snap["upstream"]["ref"], "master")
        self.assertTrue(self.snap["upstream"]["commit"])

    def test_stable_noise_consts_present(self):
        c = self.snap["consts"]
        for name in ("MAX_MESSAGE_SIZE", "TAG_SIZE", "PUBKEY_SIZE", "EPOCH_SIZE", "REPLAY_WINDOW_SIZE"):
            self.assertIn(name, c)

    def test_records_drift_field(self):
        self.assertIsInstance(self.snap["missing_expected"]["consts"], list)
        self.assertIsInstance(self.snap["missing_expected"]["enums"], list)


if __name__ == "__main__":
    unittest.main()
