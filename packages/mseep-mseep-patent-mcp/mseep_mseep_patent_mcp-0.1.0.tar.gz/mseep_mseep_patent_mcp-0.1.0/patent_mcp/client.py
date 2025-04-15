import requests
import json
from typing import Dict, Any
import os
from dotenv import load_dotenv

class PatentAPIClient:
    def __init__(self):
        load_dotenv()
        self.base_url = "https://api.patentsview.org/patents"
        
    def search_patents(self, query_params: Dict[str, Any]) -> Dict:
        """
        Search for patents using the PatentsView API
        """
        try:
            # Convert query params to PatentsView format
            search_criteria = {
                "q": {
                    "_and": [
                        {
                            "_or": [
                                {
                                    "_text_phrase": {
                                        "patent_title": "quantum computing"
                                    }
                                },
                                {
                                    "_and": [
                                        {
                                            "_text_all": {
                                                "patent_abstract": ["quantum", "computing"]
                                            }
                                        },
                                        {
                                            "_or": [
                                                {"cpc_subgroup_id": "G06N10"}, # Quantum computing
                                                {"cpc_subgroup_id": "G06N99"}, # Computing arrangements
                                                {"cpc_subgroup_id": "H01L39"}, # Superconducting devices
                                                {"cpc_subgroup_id": "G06N7"} # Probabilistic computing
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "_gte": {
                                "patent_date": query_params['start']
                            }
                        },
                        {
                            "_lte": {
                                "patent_date": query_params['end']
                            }
                        }
                    ]
                },
                "f": [
                    # Basic patent information
                    "patent_number", 
                    "patent_title", 
                    "patent_date", 
                    "patent_type", 
                    "patent_abstract",
                    "patent_kind",
                    "patent_processing_time",
                    
                    # Assignee information
                    "assignee_id",
                    "assignee_organization",
                    "assignee_type",
                    "assignee_city",
                    "assignee_state",
                    "assignee_country",
                    
                    # Inventor information
                    "inventor_id",
                    "inventor_first_name",
                    "inventor_last_name",
                    "inventor_city",
                    "inventor_state",
                    "inventor_country",
                    
                    # CPC classification
                    "cpc_section_id",
                    "cpc_subsection_id",
                    "cpc_group_id",
                    "cpc_subgroup_id",
                    "cpc_sequence",
                    
                    # Citation information
                    "cited_patent_number",
                    "cited_patent_title",
                    "cited_patent_date"
                ],
                "o": {
                    "page": query_params['pageNumber'], 
                    "per_page": query_params['pageSize'],
                    "sort": ["patent_date desc"]
                }
            }
            
            # Print request details for debugging
            print(f"Making request to: {self.base_url}/query")
            print(f"Query params: {json.dumps(search_criteria, indent=2)}")
            
            response = requests.post(
                f"{self.base_url}/query",
                json=search_criteria,
                headers={'Content-Type': 'application/json'}
            )
            
            # Print response status and headers for debugging
            print(f"Response status: {response.status_code}")
            if response.status_code != 200:
                print(f"Response text: {response.text}")
            
            response.raise_for_status()
            result = response.json()
            
            # Transform response to match expected format
            return {
                'total_patent_count': result.get('total_patent_count', 0),
                'patents': [{
                    'patentNumber': patent.get('patent_number'),
                    'title': patent.get('patent_title'),
                    'date': patent.get('patent_date'),
                    'type': patent.get('patent_type'),
                    'kind': patent.get('patent_kind'),
                    'abstract': patent.get('patent_abstract'),
                    'processingTime': patent.get('patent_processing_time'),
                    
                    # Assignee details
                    'assignee': {
                        'id': patent.get('assignee_id'),
                        'organization': patent.get('assignee_organization'),
                        'type': patent.get('assignee_type'),
                        'location': {
                            'city': patent.get('assignee_city'),
                            'state': patent.get('assignee_state'),
                            'country': patent.get('assignee_country')
                        }
                    },
                    
                    # Inventor details
                    'inventor': {
                        'id': patent.get('inventor_id'),
                        'name': f"{patent.get('inventor_first_name', '')} {patent.get('inventor_last_name', '')}".strip(),
                        'location': {
                            'city': patent.get('inventor_city'),
                            'state': patent.get('inventor_state'),
                            'country': patent.get('inventor_country')
                        }
                    },
                    
                    # CPC Classification
                    'cpc': {
                        'section': patent.get('cpc_section_id'),
                        'subsection': patent.get('cpc_subsection_id'),
                        'group': patent.get('cpc_group_id'),
                        'subgroup': patent.get('cpc_subgroup_id'),
                        'sequence': patent.get('cpc_sequence')
                    },
                    
                    # Citation information
                    'citations': [{
                        'patentNumber': num,
                        'title': title,
                        'date': date
                    } for num, title, date in zip(
                        patent.get('cited_patent_number', []),
                        patent.get('cited_patent_title', []),
                        patent.get('cited_patent_date', [])
                    )] if patent.get('cited_patent_number') else []
                } for patent in result.get('patents', [])]
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {str(e)}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Response text: {e.response.text}")
            return {}