"""Regression tests for genotype/zygosity classification.

The bug these guard against: consumer arrays report a SINGLE-character genotype
at haploid loci — every mitochondrial variant (for everyone) and the
non-pseudoautosomal X/Y in males. The original code only recognised diploid
homozygosity ("GG"), so a homoplasmic mtDNA or hemizygous X variant was
silently downgraded from AFFECTED to "heterozygous, inheritance unclear" — a
medical undercall that hides a real finding in the softest bucket.

Pure-logic tests; no ClinVar read, no network, stdlib only.
Run: python3 -m unittest discover -s tests   (from the scripts/ dir)
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from run_full_analysis import genotype_call, classify_zygosity


class TestGenotypeCall(unittest.TestCase):
    def test_diploid_homozygous_alt(self):
        has_variant, hom, hemi, het, ref_only = genotype_call("AA", "G", "A")
        self.assertTrue(has_variant)
        self.assertTrue(hom)
        self.assertFalse(hemi)
        self.assertFalse(het)

    def test_diploid_heterozygous(self):
        has_variant, hom, hemi, het, ref_only = genotype_call("GA", "G", "A")
        self.assertTrue(has_variant)
        self.assertFalse(hom)
        self.assertFalse(hemi)
        self.assertTrue(het)

    def test_diploid_ref_only(self):
        has_variant, hom, hemi, het, ref_only = genotype_call("GG", "G", "A")
        self.assertFalse(has_variant)
        self.assertTrue(ref_only)

    def test_haploid_variant_is_hemizygous_not_heterozygous(self):
        # mtDNA homoplasmic / male X hemizygous: single char equal to alt.
        has_variant, hom, hemi, het, ref_only = genotype_call("A", "G", "A")
        self.assertTrue(has_variant)
        self.assertFalse(hom)
        self.assertTrue(hemi)          # the fix
        self.assertFalse(het)          # must NOT be called heterozygous
        self.assertFalse(ref_only)

    def test_haploid_ref_only(self):
        has_variant, hom, hemi, het, ref_only = genotype_call("G", "G", "A")
        self.assertFalse(has_variant)
        self.assertFalse(hemi)
        self.assertTrue(ref_only)


class TestClassifyZygosity(unittest.TestCase):
    def _finding(self, **kw):
        base = dict(is_homozygous=False, is_hemizygous=False,
                    is_heterozygous=False, inheritance="")
        base.update(kw)
        return base

    def test_homozygous_is_affected(self):
        status, _ = classify_zygosity(self._finding(is_homozygous=True))
        self.assertEqual(status, "AFFECTED")

    def test_hemizygous_is_affected(self):
        # was UNKNOWN before the fix
        status, _ = classify_zygosity(self._finding(is_hemizygous=True))
        self.assertEqual(status, "AFFECTED")

    def test_het_recessive_is_carrier(self):
        status, _ = classify_zygosity(
            self._finding(is_heterozygous=True, inheritance="autosomal recessive"))
        self.assertEqual(status, "CARRIER")

    def test_het_dominant_is_affected(self):
        status, _ = classify_zygosity(
            self._finding(is_heterozygous=True, inheritance="autosomal dominant"))
        self.assertEqual(status, "AFFECTED")

    def test_het_unclear_is_heterozygous(self):
        status, _ = classify_zygosity(self._finding(is_heterozygous=True))
        self.assertEqual(status, "HETEROZYGOUS")


if __name__ == "__main__":
    unittest.main()
