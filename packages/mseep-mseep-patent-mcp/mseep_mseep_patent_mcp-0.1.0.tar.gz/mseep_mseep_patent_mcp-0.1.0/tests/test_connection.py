import asyncio
from patent_mcp.client import PatentAPIClient

def format_assignee(assignee):
    if not assignee.get('organization'):
        return 'Not specified'
    location = assignee.get('location', {})
    location_str = f"{location.get('city', '')}, {location.get('state', '')}, {location.get('country', '')}".strip(', ')
    return f"{assignee['organization']} ({location_str}) [{assignee.get('type', 'Unknown type')}]"

def format_inventor(inventor):
    if not inventor.get('name'):
        return 'Not specified'
    location = inventor.get('location', {})
    location_str = f"{location.get('city', '')}, {location.get('state', '')}, {location.get('country', '')}".strip(', ')
    return f"{inventor['name']} ({location_str})"

def format_cpc(cpc):
    if not cpc.get('section'):
        return 'Not specified'
    return f"{cpc['section']}/{cpc.get('subsection', '')} - {cpc.get('group', '')}/{cpc.get('subgroup', '')} (Sequence: {cpc.get('sequence', 'Unknown')})"

async def test_api_connection():
    client = PatentAPIClient()
    
    # Test simple search
    test_query = {
        'searchText': 'quantum computing',
        'start': '2023-01-01',
        'end': '2024-12-31',
        'pageSize': 5,
        'pageNumber': 1
    }
    
    print('\nTesting PatentsView API connection...')
    try:
        results = client.search_patents(test_query)
        if results and results.get('patents'):
            print('\n✅ Connection successful!')
            print(f'Total patents found: {results.get("total_patent_count", 0)}')
            print(f'Showing {len(results["patents"])} results from page {test_query["pageNumber"]}')
            print('\nSample results:')
            
            for patent in results['patents']:
                print(f'\n{"-"*80}')
                print(f'Title: {patent["title"]}')
                print(f'Patent Number: {patent["patentNumber"]}')
                print(f'Date: {patent["date"]}')
                print(f'Type: {patent["type"]} ({patent["kind"]})')
                
                print(f'\nAssignee: {format_assignee(patent["assignee"])}')
                print(f'Inventor: {format_inventor(patent["inventor"])}')
                
                print(f'\nCPC Classification: {format_cpc(patent["cpc"])}')
                
                if patent.get('abstract'):
                    print(f'\nAbstract: {patent["abstract"][:200]}...')
                
                if patent.get('citations'):
                    print(f'\nCitations ({len(patent["citations"])} patents):')
                    for citation in patent['citations'][:3]:  # Show first 3 citations
                        print(f"  - {citation['patentNumber']}: {citation['title']} ({citation['date']})")
                    if len(patent['citations']) > 3:
                        print(f"  ... and {len(patent['citations']) - 3} more")
                
                print(f'\nProcessing Time: {patent.get("processingTime", "Not specified")} days')
        else:
            print('\n❌ No results returned')
    except Exception as e:
        print(f'\n❌ Error: {str(e)}')

if __name__ == '__main__':
    asyncio.run(test_api_connection())