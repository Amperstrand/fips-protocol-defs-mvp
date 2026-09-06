import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))

from check_consumer_drift import extract_constants, main, compare  # noqa: E402


PROFILE = '''
pub const PROFILE_NAME: &str = "fips-v0-ik-xk";
pub const FMP_VERSION: u8 = 0;
pub const COMMON_PREFIX_SIZE: usize = 4;
pub const HANDSHAKE_MSG1_SIZE: usize = 106;
pub const TAG_SIZE: usize = 16;
'''

CONSUMER_MATCHING = '''
pub const TAG_SIZE: usize = 16;
pub const FMP_VERSION: u8 = 0;
pub const COMMON_PREFIX_SIZE: usize = 4;
pub const HANDSHAKE_MSG1_SIZE: usize = 86 + 2 * TAG_SIZE; // derived
pub const CONSUMER_ONLY: usize = 7;
'''

CONSUMER_DRIFTED = '''
pub const FMP_VERSION: u8 = 1;
pub const TAG_SIZE: usize = 16;
'''


class CheckConsumerDriftTests(unittest.TestCase):
    def test_extracts_literals_and_derived(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'c.rs'
            p.write_text(CONSUMER_MATCHING)
            consts = extract_constants(str(p))
        self.assertEqual(consts['FMP_VERSION'], 0)
        self.assertEqual(consts['HANDSHAKE_MSG1_SIZE'], 118)  # 86 + 2*16
        self.assertEqual(consts['CONSUMER_ONLY'], 7)

    def test_matching_consumer_passes(self):
        with tempfile.TemporaryDirectory() as td:
            pp, cp = Path(td) / 'p.rs', Path(td) / 'c.rs'
            pp.write_text(PROFILE)
            cp.write_text(CONSUMER_MATCHING)
            rc = main([str(pp), str(cp), '--fail-on-drift'])
        self.assertEqual(rc, 0)

    def test_drift_fails(self):
        with tempfile.TemporaryDirectory() as td:
            pp, cp = Path(td) / 'p.rs', Path(td) / 'c.rs'
            pp.write_text(PROFILE)
            cp.write_text(CONSUMER_DRIFTED)
            drift, compared = compare(
                extract_constants(str(pp)), extract_constants(str(cp)))
        self.assertEqual(compared, 2)
        self.assertEqual(drift, [('FMP_VERSION', 0, 1)])


if __name__ == '__main__':
    unittest.main()
