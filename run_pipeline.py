import os
import json
import datetime
from src.client import GeminiClient
from src.generator import EmailReplyGenerator
from src.evaluator import ResponseEvaluator

def print_banner(text: str, width: int = 80):
    print("=" * width)
    print(text.center(width))
    print("=" * width)

def main():
    print_banner("HIVIER AI EMAIL SUGGESTED-RESPONSE PIPELINE")
    
    # 1. Initialize Gemini Client (checks keys & activates simulation fallback)
    client = GeminiClient()
    
    if client.is_simulation_mode:
        print("[STATUS] [SIMULATION] Running in SIMULATION Mode. No API key found.")
        print("         Generator will use high-fidelity mock replies.")
        print("         Evaluator will run lexical evaluation & proxy grading.")
    else:
        print("[STATUS] [LIVE] Running in LIVE API Mode. Gemini API key detected.")
        print("         Generating real-time suggestions using 'gemini-2.5-flash'.")
        print("         Evaluating semantic quality using LLM-as-a-Judge.")
    print()

    # 2. Check that datasets exist
    support_path = os.path.join("data", "support_dataset.json")
    test_path = os.path.join("data", "test_queries.json")
    
    if not os.path.exists(support_path) or not os.path.exists(test_path):
        print("[ERROR] Datasets missing! Please run 'python generate_dataset.py' first.")
        return

    # 3. Instantiate modules
    generator = EmailReplyGenerator(support_path, client)
    evaluator = ResponseEvaluator(client)

    # 4. Load test queries
    with open(test_path, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    print(f"Loaded {len(test_cases)} test email cases to process.\n")
    results = []

    # 5. Process and evaluate each case
    for idx, case in enumerate(test_cases, 1):
        print(f"Processing Case {idx}/{len(test_cases)}: ID={case['id']} | Category={case['category']}")
        print(f"Subject: {case.get('subject', '')}")
        print(f"Customer: {case.get('customer_email', '')}")
        print("-" * 50)
        
        # Generate reply
        gen_output = generator.generate_response(case)
        generated_reply = gen_output["generated_reply"]
        
        # Evaluate reply
        eval_output = evaluator.evaluate_response(
            incoming_email=case["incoming_body"],
            target_reply=case["target_reply"],
            generated_reply=generated_reply
        )
        
        # Store results
        results.append({
            "id": case["id"],
            "category": case["category"],
            "subject": case["subject"],
            "customer_email": case["customer_email"],
            "incoming_body": case["incoming_body"],
            "target_reply": case["target_reply"],
            "generated_reply": generated_reply,
            "retrieved_context": gen_output["retrieved_context"],
            "scores": eval_output
        })
        
        # Display scores
        print(f"Scores:")
        print(f"  - Lexical Score (Vocabulary Cosine): {eval_output['lexical_score']}%")
        print(f"  - Semantic Score (LLM-as-a-Judge):    {eval_output['semantic_score']}%")
        print(f"  - Hybrid Evaluated Score:           {eval_output['hybrid_score']}%")
        print(f"Evaluation Mode: {eval_output['evaluation_mode']}")
        print("-" * 50)
        print("Generated Reply Sample:")
        first_lines = "\n".join(generated_reply.split("\n")[:4])
        print(first_lines + ("\n..." if len(generated_reply.split("\n")) > 4 else ""))
        print("=" * 80 + "\n")

    # 6. Compute aggregate stats
    overall_stats = evaluator.compute_overall_stats(results)
    
    # 7. Print dashboard report
    print_banner("SYSTEM ACCURACY & EVALUATION SUMMARY REPORT")
    print(f"Timestamp:             {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Evaluation Engine:     {results[0]['scores']['evaluation_mode']}")
    print(f"Total Emails Processed: {overall_stats['total_evaluated']}")
    print(f"Average Lexical Score:  {overall_stats['avg_lexical_score']}%")
    print(f"Average Semantic Score: {overall_stats['avg_semantic_score']}%")
    print("-" * 40)
    print(f"OVERALL HYBRID SCORE:   {overall_stats['avg_hybrid_score']}%")
    print(f"Min / Max Hybrid Score: {overall_stats['min_hybrid_score']}% / {overall_stats['max_hybrid_score']}%")
    print(f"System Pass Rate:       {overall_stats['pass_rate_percentage']}% (Hybrid Score >= 75%)")
    print("=" * 80)

    # 8. Save Detailed Reports (JSON + Markdown)
    report_data = {
        "overall_summary": overall_stats,
        "mode": results[0]['scores']['evaluation_mode'],
        "timestamp": datetime.datetime.now().isoformat(),
        "test_results": results
    }
    
    # Save JSON report
    report_json_path = os.path.join("data", "evaluation_report.json")
    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    print(f"\n[SAVED] Detailed JSON evaluation report written to: {report_json_path}")

    # Generate and Save Markdown report for clear documentation
    report_md_path = os.path.join("data", "evaluation_report.md")
    write_markdown_report(report_md_path, report_data)
    print(f"[SAVED] Formatted Markdown evaluation report written to: {report_md_path}")

def write_markdown_report(filepath: str, report_data: Dict):
    summary = report_data["overall_summary"]
    
    md_content = f"""# Hiver AI Suggestion Pipeline - Evaluation Report

**Generated:** {report_data['timestamp']}  
**Evaluation Mode:** `{report_data['mode']}`

## System Performance Summary

| Metric | Score |
| :--- | :--- |
| **Total Test Cases** | {summary['total_evaluated']} |
| **Average Lexical Score** | {summary['avg_lexical_score']}% |
| **Average Semantic Score** | {summary['avg_semantic_score']}% |
| **Overall Hybrid Accuracy** | **{summary['avg_hybrid_score']}%** |
| **Min / Max Score** | {summary['min_hybrid_score']}% / {summary['max_hybrid_score']}% |
| **Pass Rate (>=75.0% Hybrid)** | **{summary['pass_rate_percentage']}%** |

---

## Detailed Per-Response Scores

"""
    for res in report_data["test_results"]:
        scores = res["scores"]
        md_content += f"""### Test Case `{res['id']}` - Category: `{res['category']}`
* **Subject:** {res['subject']}
* **Customer Email:** `{res['customer_email']}`
* **RAG Retrieved Historical Examples:** {', '.join([f"`{c['id']}` (Score: {c['score']:.2f})" for c in res['retrieved_context']])}

#### Scores
* **Lexical Score (Overlap):** `{scores['lexical_score']}%`
* **Semantic Score (LLM-as-a-Judge):** `{scores['semantic_score']}%`
* **Hybrid Evaluation Score:** **`{scores['hybrid_score']}%`**

#### Criteria Grades
* **Factual Correctness (0-10):** `{scores['criteria']['factual_correctness']['score']}` - *{scores['criteria']['factual_correctness']['reason']}*
* **Tone & Professionalism (0-5):** `{scores['criteria']['tone_professionalism']['score']}` - *{scores['criteria']['tone_professionalism']['reason']}*
* **Completeness (0-5):** `{scores['criteria']['completeness']['score']}` - *{scores['criteria']['completeness']['reason']}*
* **No Hallucination (0-5):** `{scores['criteria']['no_hallucination']['score']}` - *{scores['criteria']['no_hallucination']['reason']}*

<details>
<summary><b>Show Generated Reply</b></summary>

```email
{res['generated_reply']}
```
</details>

<details>
<summary><b>Show Target Gold Standard Reply</b></summary>

```email
{res['target_reply']}
```
</details>

---
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md_content)

if __name__ == "__main__":
    main()
