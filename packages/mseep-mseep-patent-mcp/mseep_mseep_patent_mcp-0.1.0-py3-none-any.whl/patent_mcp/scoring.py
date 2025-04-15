from typing import Dict

class PatentScoring:
    def __init__(self):
        self.weight_citations = 0.3
        self.weight_claims = 0.2
        self.weight_family = 0.2
        self.weight_age = 0.15
        self.weight_legal = 0.15

    def calculate_pscore(self, patent_data: Dict) -> float:
        """
        Calculate patent score based on multiple factors
        """
        # Basic normalization function
        normalize = lambda x, min_val, max_val: (x - min_val) / (max_val - min_val) if max_val > min_val else 0

        # Extract relevant metrics
        num_claims = len(patent_data.get('claims', []))
        num_citations = len(patent_data.get('citations', []))
        family_size = len(patent_data.get('family_members', []))

        # Normalize values (example ranges, adjust based on actual data)
        claims_score = normalize(num_claims, 0, 50)
        citations_score = normalize(num_citations, 0, 100)
        family_score = normalize(family_size, 0, 20)

        # Calculate weighted score
        pscore = (
            self.weight_claims * claims_score +
            self.weight_citations * citations_score +
            self.weight_family * family_score
        )

        return min(max(pscore * 100, 0), 100)

    def calculate_cscore(self, patent_data: Dict) -> float:
        """
        Calculate citation score based on citation analysis
        """
        citations = patent_data.get('citations', [])
        if not citations:
            return 0

        forward_citations = len([c for c in citations if c.get('type') == 'forward'])
        backward_citations = len([c for c in citations if c.get('type') == 'backward'])

        # Weight forward citations more heavily
        cscore = (forward_citations * 1.5 + backward_citations) / (len(citations) * 1.5)
        return min(cscore * 100, 100)

    def calculate_lscore(self, patent_data: Dict) -> float:
        """
        Calculate legal score based on legal status and history
        """
        status = patent_data.get('legal_status', {})
        base_score = 50  # Start with neutral score

        # Adjust based on status
        if status.get('active', False):
            base_score += 25
        if not status.get('opposition_filed', False):
            base_score += 15
        if status.get('grant_date'):
            base_score += 10

        return min(base_score, 100)

    def calculate_tscore(self, patent_data: Dict) -> float:
        """
        Calculate technology score based on technical factors
        """
        # Initialize base score
        base_score = 50

        # Adjust based on CPC codes
        cpc_codes = patent_data.get('cpc_codes', [])
        if len(cpc_codes) > 3:
            base_score += 15

        # Adjust based on technical complexity
        claims = patent_data.get('claims', [])
        if len(claims) > 20:
            base_score += 10

        # Adjust based on drawings/figures
        figures = patent_data.get('figures', [])
        if len(figures) > 5:
            base_score += 10

        return min(base_score, 100)