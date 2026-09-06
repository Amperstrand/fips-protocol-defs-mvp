"""Cross-vectors validation (P5): vectors/fips-v0-cross-vectors.json is the
canonical file every FIPS-adjacent home pins against. This test keeps the
file honest against the profile source of truth — sizes, type table, and the
golden msg1 — so drift between profile, generated output, and vectors fails
here first."""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VECTORS = json.loads((ROOT / 'vectors' / 'fips-v0-cross-vectors.json').read_text())
PROFILE = json.loads((ROOT / 'profiles' / 'fips-v0-ik-xk.json').read_text())
GOLDEN = json.loads((ROOT / 'fixtures' / 'noise_ik_golden.json').read_text())
GENERATED_RUST = (ROOT / 'generated' / 'rust' / 'fips_v0_ik_xk.rs').read_text()


class LinkMessageTypesTests(unittest.TestCase):
    def test_vector_table_matches_profile(self):
        profile_types = PROFILE['link']['message_types']
        for v in VECTORS['link_message_types']['vectors']:
            self.assertIn('0x' + v['type'], profile_types,
                          f"type {v['type']} missing from profile")
            self.assertEqual(profile_types['0x' + v['type']], v['name'])
        self.assertEqual(len(VECTORS['link_message_types']['vectors']),
                         len(profile_types), 'vector table out of sync with profile size')

    def test_table_present_in_generated_rust(self):
        for v in VECTORS['link_message_types']['vectors']:
            self.assertIn(v['name'], GENERATED_RUST)


class FrameLayoutTests(unittest.TestCase):
    def test_msg_sizes_match_profile(self):
        fmp = PROFILE['fmp']
        sizes = {v['frame']: v['total_size']
                 for v in VECTORS['fmp_frame_layouts']['vectors']}
        self.assertEqual(fmp['messages']['msg1']['wire_size'] + 8, sizes['msg1_wire'])
        self.assertEqual(fmp['messages']['msg2']['wire_size'] + 12, sizes['msg2_wire'])


class GoldenMsg1Tests(unittest.TestCase):
    def test_msg1_identical_to_golden_fixture(self):
        g = VECTORS['noise_ik_msg1_golden']
        self.assertEqual(g['msg1_hex'], GOLDEN['microfips_generated_msg1'])
        self.assertEqual(g['init_static_secret'], GOLDEN['init_static_secret'])
        self.assertEqual(len(bytes.fromhex(g['msg1_hex'])), g['msg1_len'])

    def test_msg1_length_matches_profile(self):
        self.assertEqual(PROFILE['fmp']['messages']['msg1']['wire_size'],
                         VECTORS['noise_ik_msg1_golden']['msg1_len'])

    def test_msg1_leads_with_ephemeral_pubkey(self):
        g = VECTORS['noise_ik_msg1_golden']
        # Noise IK msg1 = ephemeral pubkey || encrypted(static, epoch); the
        # static key itself must NOT appear in plaintext.
        self.assertIn(g['msg1_hex'][:2], ('02', '03'))
        self.assertNotIn(g['init_static_pub'][2:], g['msg1_hex'],
                         'static pubkey leaked in plaintext in msg1')


if __name__ == '__main__':
    unittest.main()
