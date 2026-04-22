import os
import click
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from dotenv import load_dotenv

load_dotenv()

# GraphQL Query
STARS_QUERY = gql("""
query($username: String!, $after: String) {
  user(login: $username) {
    starredRepositories(first: 100, after: $after, orderBy: {field: STARRED_AT, direction: DESC}) {
      pageInfo {
        endCursor
        hasNextPage
      }
      edges {
        node {
          nameWithOwner
          description
          url
          stargazerCount
          primaryLanguage {
            name
          }
          repositoryTopics(first: 10) {
            nodes {
              topic {
                name
              }
            }
          }
        }
      }
    }
  }
}
""")

def get_all_stars(username, token):
    transport = RequestsHTTPTransport(
        url='https://api.github.com/graphql',
        headers={'Authorization': f'Bearer {token}'},
        use_json=True,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)
    
    stars = []
    after = None
    has_next_page = True
    
    click.echo(f"Fetching stars for {username}...")
    
    while has_next_page:
        params = {"username": username, "after": after}
        result = client.execute(STARS_QUERY, variable_values=params)
        
        data = result['user']['starredRepositories']
        for edge in data['edges']:
            node = edge['node']
            repo = {
                'name': node['nameWithOwner'],
                'description': node['description'],
                'url': node['url'],
                'stars': node['stargazerCount'],
                'language': node['primaryLanguage']['name'] if node['primaryLanguage'] else 'Others',
                'topics': [t['topic']['name'] for t in node['repositoryTopics']['nodes']]
            }
            stars.append(repo)
        
        after = data['pageInfo']['endCursor']
        has_next_page = data['pageInfo']['hasNextPage']
        click.echo(f"Fetched {len(stars)} stars...")
        
    return stars

def generate_markdown(stars, groupby='language'):
    grouped = {}
    for repo in stars:
        key = repo.get(groupby, 'Others')
        if groupby == 'topics':
            # If grouping by topics, a repo might appear in multiple sections
            keys = repo['topics'] if repo['topics'] else ['No Topic']
            for k in keys:
                grouped.setdefault(k, []).append(repo)
        else:
            grouped.setdefault(key, []).append(repo)
            
    content = f"""---
title: "星标项目"
date: {datetime.now().strftime('%Y-%m-%d')}
layout: "single"
showtoc: true
---

# My GitHub Stars

"""
    content += f"Total stars: {len(stars)}\n\n"
    
    # Table of Contents
    content += "## Table of Contents\n\n"
    sorted_keys = sorted(grouped.keys())
    for key in sorted_keys:
        anchor = key.lower().replace(' ', '-').replace('.', '')
        content += f"- [{key}](#{anchor})\n"
    content += "\n"
    
    # Sections
    for key in sorted_keys:
        content += f"## {key}\n\n"
        for repo in grouped[key]:
            description = repo['description'] if repo['description'] else "No description"
            content += f"- [{repo['name']}]({repo['url']}) - {description} (★{repo['stars']})\n"
        content += "\n"
        
    return content

@click.command()
@click.option('--username', default=lambda: os.environ.get('GITHUB_USERNAME'), help='GitHub username')
@click.option('--token', default=lambda: os.environ.get('GITHUB_TOKEN'), help='GitHub token')
@click.option('--output', default='README.md', help='Output file name')
@click.option('--groupby', type=click.Choice(['language', 'topics']), default='language', help='Group by language or topics')
def main(username, token, output, groupby):
    if not username or not token:
        click.echo("Error: GITHUB_USERNAME and GITHUB_TOKEN must be provided (via args or .env)")
        return
        
    try:
        stars = get_all_stars(username, token)
        md_content = generate_markdown(stars, groupby)
        
        with open(output, 'w', encoding='utf-8') as f:
            f.write(md_content)
            
        click.echo(f"Successfully generated {output} with {len(stars)} stars.")
    except Exception as e:
        click.echo(f"Error: {e}")

if __name__ == '__main__':
    main()
