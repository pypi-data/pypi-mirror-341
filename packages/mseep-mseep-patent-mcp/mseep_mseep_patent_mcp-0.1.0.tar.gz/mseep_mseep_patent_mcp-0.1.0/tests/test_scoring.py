import unittest
from patent_mcp.scoring import PatentScoring

class TestPatentScoring(unittest.TestCase):
    def setUp(self):
        self.scoring = PatentScoring()

    def test_pscore_calculation(self):
        test_patent = {
            'claims': ['claim1', 'claim2', 'claim3'],
            'citations': ['cite1', 'cite2'],
            'family_members': ['family1']
        }
        score = self.scoring.calculate_pscore(test_patent)
        self.assertTrue(0 <= score <= 100)

    def test_cscore_calculation(self):
        test_patent = {
            'citations': [
                {'type': 'forward'},
                {'type': 'backward'},
                {'type': 'forward'}
            ]
        }
        score = self.scoring.calculate_cscore(test_patent)
        self.assertTrue(0 <= score <= 100)

if __name__ == '__main__':
    unittest.main()