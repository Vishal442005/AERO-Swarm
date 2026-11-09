#!/usr/bin/env python3
"""
Fetch and download the most recent papers published in:
- Swarm and Evolutionary Computation (SWEVO) [Elsevier, ISSN: 2210-6502, OpenAlex: S2764346689]
- Robotics and Autonomous Systems (RAS) [Elsevier, ISSN: 0921-8890, OpenAlex: S133768115]

Scope: UAV / Drone Swarms, Multi-Agent Coordination, Resilient Consensus,
Task Allocation / Auctions, Communication Constraints, Obstacle Avoidance.
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")

import json
import os
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

OUTPUT_DIR = Path("papers/swevo_ras_recent")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

SOURCES = {
    "SWEVO": {
        "id": "S2764346689",
        "name": "Swarm and Evolutionary Computation",
        "queries": [
            "UAV OR drone OR multi-robot OR robot swarm",
            "task allocation OR auction OR consensus",
            "swarm resilience OR obstacle avoidance"
        ]
    },
    "RAS": {
        "id": "S133768115",
        "name": "Robotics and Autonomous Systems",
        "queries": [
            "UAV swarm OR drone swarm OR multi-robot swarm",
            "task allocation OR consensus OR formation",
            "communication delays OR communication restricted"
        ]
    }
}

def reconstruct_abstract(inv_idx):
    if not inv_idx:
        return ""
    words = []
    for word, positions in inv_idx.items():
        for pos in positions:
            words.append((pos, word))
    words.sort()
    return " ".join(w[1] for w in words)

def safe_filename(title, max_len=60):
    clean = re.sub(r'[^\w\-_\. ]', '_', title)
    clean = re.sub(r'\s+', '_', clean)
    return clean[:max_len].strip('_')

def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "AERO-Swarm/1.0 (mailto:chandelvishal445@gmail.com)"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def download_file(url, target_path):
    if not url:
        return False
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/pdf,application/octet-stream,*/*",
        "Referer": "https://scholar.google.com/"
    })
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            content_type = resp.headers.get("Content-Type", "")
            data = resp.read()
            if len(data) > 5000 and (data[:4] == b"%PDF" or "pdf" in content_type.lower()):
                with open(target_path, "wb") as f:
                    f.write(data)
                print(f"    [DOWNLOADED PDF] {target_path.name} ({len(data):,} bytes)")
                return True
            else:
                return False
    except Exception as e:
        return False

def search_journal(journal_key, journal_info):
    collected_works = {}
    print(f"\n========================================================")
    print(f"Querying OpenAlex for {journal_key}: {journal_info['name']}")
    print(f"========================================================")
    
    source_id = journal_info["id"]
    for q in journal_info["queries"]:
        encoded_q = urllib.parse.quote(q)
        url = (
            f"https://api.openalex.org/works?"
            f"filter=primary_location.source.id:{source_id},publication_year:>2023"
            f"&search={encoded_q}"
            f"&sort=publication_date:desc"
            f"&per-page=25"
        )
        data = fetch_json(url)
        if not data or "results" not in data:
            continue
        
        for work in data["results"]:
            work_id = work["id"]
            if work_id not in collected_works:
                collected_works[work_id] = work
        time.sleep(0.3)

    print(f"Found {len(collected_works)} candidate works for {journal_key}.")
    return list(collected_works.values())

def find_pdf_candidates(work):
    candidates = []
    
    # 1. best_oa_location pdf_url
    best_oa = work.get("best_oa_location") or {}
    if best_oa.get("pdf_url"):
        candidates.append(best_oa["pdf_url"])
        
    # 2. open_access oa_url
    oa_info = work.get("open_access", {})
    if oa_info.get("oa_url"):
        candidates.append(oa_info["oa_url"])
        
    # 3. all locations
    for loc in work.get("locations", []):
        if loc.get("pdf_url") and loc["pdf_url"] not in candidates:
            candidates.append(loc["pdf_url"])
            
    # 4. Check for SSRN or arXiv
    for loc in work.get("locations", []):
        landing = loc.get("landing_page_url") or ""
        if "arxiv.org" in landing:
            arxiv_id = landing.split("/")[-1]
            candidates.append(f"https://arxiv.org/pdf/{arxiv_id}.pdf")
        if "ssrn.com" in landing or "ssrn." in landing:
            match = re.search(r'ssrn\.(\d+)', landing)
            if match:
                s_id = match.group(1)
                candidates.append(f"https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID{s_id}_code.pdf?abstractid={s_id}&mirid=1")
                
    return candidates

def main():
    all_papers = []
    
    for j_key, j_info in SOURCES.items():
        works = search_journal(j_key, j_info)
        
        for w in works:
            w_id = w["id"].split("/")[-1]
            title = w.get("title") or "Untitled"
            doi = w.get("doi") or ""
            pub_date = w.get("publication_date") or ""
            authors = [a["author"]["display_name"] for a in w.get("authorships", []) if "author" in a]
            first_author = authors[0] if authors else "Unknown"
            
            # Keywords scoring
            title_lower = title.lower()
            relevant_keywords = [
                "uav", "drone", "swarm", "multi-robot", "agent", "consensus", 
                "task allocation", "auction", "formation", "resilience", 
                "obstacle", "path planning", "cooperative", "heterogeneous",
                "communication", "decentralized", "distributed", "flocking"
            ]
            match_count = sum(1 for kw in relevant_keywords if kw in title_lower)
            
            # Reconstruct abstract
            abstract = reconstruct_abstract(w.get("abstract_inverted_index"))
            abstract_lower = abstract.lower()
            abstract_matches = sum(1 for kw in relevant_keywords if kw in abstract_lower)
            
            # Prioritize swarm + uav/drone + task allocation/resilience
            core_bonus = 0
            if any(k in title_lower for k in ["swarm", "uav", "drone", "multi-robot"]):
                core_bonus += 5
            if any(k in title_lower for k in ["task allocation", "auction", "consensus", "resilience", "formation", "cooperative"]):
                core_bonus += 5
                
            score = match_count * 2 + (abstract_matches > 0) * 2 + core_bonus
            
            oa_info = w.get("open_access", {})
            is_oa = oa_info.get("is_oa", False)
            oa_status = oa_info.get("oa_status", "unknown")
            best_oa = w.get("best_oa_location") or {}
            landing_url = best_oa.get("landing_page_url") or doi
            pdf_candidates = find_pdf_candidates(w)
            
            all_papers.append({
                "journal": j_key,
                "journal_name": j_info["name"],
                "openalex_id": w_id,
                "title": title,
                "authors": authors,
                "first_author": first_author,
                "doi": doi,
                "pub_date": pub_date,
                "abstract": abstract,
                "is_oa": is_oa,
                "oa_status": oa_status,
                "landing_url": landing_url,
                "pdf_candidates": pdf_candidates,
                "relevance_score": score,
                "raw_work": w
            })

    # Sort papers by relevance score and recency
    top_swevo = sorted([p for p in all_papers if p["journal"] == "SWEVO"], 
                       key=lambda p: (p["relevance_score"], p["pub_date"]), reverse=True)[:6]
    top_ras = sorted([p for p in all_papers if p["journal"] == "RAS"], 
                     key=lambda p: (p["relevance_score"], p["pub_date"]), reverse=True)[:6]
    
    selected_papers = top_swevo + top_ras
    
    print(f"\n========================================================")
    print(f"Selected Top {len(selected_papers)} Papers (6 SWEVO + 6 RAS):")
    print(f"========================================================")
    
    downloaded_count = 0
    
    for idx, p in enumerate(selected_papers, 1):
        author_str = ", ".join(p['authors'][:3])
        if len(p['authors']) > 3:
            author_str += " et al."
        print(f"\n{idx}. [{p['journal']}] ({p['pub_date']}) {p['title']}")
        print(f"   Authors: {author_str}")
        print(f"   DOI: {p['doi']}")
        print(f"   OA Status: {p['oa_status']} | PDF Candidates: {len(p['pdf_candidates'])}")
        
        # Save individual metadata & abstract text
        fname_base = f"{p['journal']}_{p['pub_date'][:4]}_{safe_filename(p['title'])}"
        txt_path = OUTPUT_DIR / f"{fname_base}.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"Title: {p['title']}\n")
            f.write(f"Journal: {p['journal_name']} ({p['journal']})\n")
            f.write(f"Published Date: {p['pub_date']}\n")
            f.write(f"Authors: {', '.join(p['authors'])}\n")
            f.write(f"DOI: {p['doi']}\n")
            f.write(f"OpenAlex ID: {p['openalex_id']}\n")
            f.write(f"Open Access: {p['is_oa']} ({p['oa_status']})\n")
            f.write(f"URL: {p['landing_url']}\n")
            f.write(f"\n--- ABSTRACT ---\n{p['abstract']}\n")
            
        target_pdf = OUTPUT_DIR / f"{fname_base}.pdf"
        downloaded = False
        
        # Try downloading each PDF candidate
        for url in p["pdf_candidates"]:
            print(f"   Attempting PDF download from: {url[:80]}...")
            downloaded = download_file(url, target_pdf)
            if downloaded:
                downloaded_count += 1
                break
                
        p["pdf_downloaded"] = downloaded
        p["pdf_local_path"] = str(target_pdf) if downloaded else None
        p["txt_local_path"] = str(txt_path)
        # remove raw_work before saving JSON to keep it clean
        p.pop("raw_work", None)

    # Master summary
    summary_path = OUTPUT_DIR / "swevo_ras_recent_papers_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(selected_papers, f, indent=2, ensure_ascii=False)
        
    print(f"\n========================================================")
    print(f"Download Finished! {downloaded_count}/{len(selected_papers)} PDFs saved directly.")
    print(f"All 12 full text abstracts and metadata written to {OUTPUT_DIR}")
    print(f"Master summary written to {summary_path}")
    print(f"========================================================")

if __name__ == "__main__":
    main()
