# Hiver AI Suggestion Pipeline - Evaluation Report

**Generated:** 2026-07-06T16:40:46.300138  
**Evaluation Mode:** `Simulated-Proxy`

## System Performance Summary

| Metric | Score |
| :--- | :--- |
| **Total Test Cases** | 5 |
| **Average Lexical Score** | 68.97% |
| **Average Semantic Score** | 87.19% |
| **Overall Hybrid Accuracy** | **79.9%** |
| **Min / Max Score** | 69.87% / 86.54% |
| **Pass Rate (>=75.0% Hybrid)** | **80.0%** |

---

## Detailed Per-Response Scores

### Test Case `test_1` - Category: `billing_refund`
* **Subject:** Charged for subscription after cancelling
* **Customer Email:** `tom.jones@example.com`
* **RAG Retrieved Historical Examples:** `hist_2` (Score: 0.41), `hist_17` (Score: 0.26)

#### Scores
* **Lexical Score (Overlap):** `70.06%`
* **Semantic Score (LLM-as-a-Judge):** `90.02%`
* **Hybrid Evaluation Score:** **`82.03%`**

#### Criteria Grades
* **Factual Correctness (0-10):** `7.5` - *Simulated evaluation based on lexical overlap proxy.*
* **Tone & Professionalism (0-5):** `5.0` - *Polite sign-off and structured greeting are present.*
* **Completeness (0-5):** `5.0` - *Successfully addresses the keywords matching customer request.*
* **No Hallucination (0-5):** `5.0` - *Vocabulary stays close to the matched context templates.*

<details>
<summary><b>Show Generated Reply</b></summary>

```email
Hi Tom,

Thanks for reaching out. I checked your account status and verified that your cancellation did not register in time for the billing cycle, resulting in the $25 charge.

I have now finalized your account cancellation and initiated a full refund of $25.00 back to your card. Please allow 5-10 business days for the credit to appear. We apologize for the error!

Best regards,
Sarah
Customer Support Team
```
</details>

<details>
<summary><b>Show Target Gold Standard Reply</b></summary>

```email
Hi Tom,

Thanks for reaching out. I reviewed your account settings and confirmed that your cancellation did not finalize correctly before the billing run, which caused the $25.00 charge. 

I have finalized the cancellation of your subscription and processed a full refund of $25.00. You should see the credit on your bank statement in 5-10 business days.

We apologize for this system error and hope to welcome you back in the future.

Best regards,
Sarah
Customer Support Team
```
</details>

---
### Test Case `test_2` - Category: `technical_bug`
* **Subject:** Cannot upload profile picture
* **Customer Email:** `maria.gomez@example.com`
* **RAG Retrieved Historical Examples:** `hist_5` (Score: 0.14), `hist_15` (Score: 0.13)

#### Scores
* **Lexical Score (Overlap):** `65.0%`
* **Semantic Score (LLM-as-a-Judge):** `84.0%`
* **Hybrid Evaluation Score:** **`76.4%`**

#### Criteria Grades
* **Factual Correctness (0-10):** `7.0` - *Simulated evaluation based on lexical overlap proxy.*
* **Tone & Professionalism (0-5):** `5.0` - *Polite sign-off and structured greeting are present.*
* **Completeness (0-5):** `4.0` - *Successfully addresses the keywords matching customer request.*
* **No Hallucination (0-5):** `5.0` - *Vocabulary stays close to the matched context templates.*

<details>
<summary><b>Show Generated Reply</b></summary>

```email
Hi Maria,

I'm sorry you are having trouble uploading your profile photo. Please note that our system restricts profile picture uploads to a maximum size of 1.5MB.

Since your JPEG is 2MB, the system rejected it. Please try compression to get it under 1.5MB and upload it again. If the issue persists, feel free to email the image to me and I will upload it for you.

Best,
Alex
Technical Support Team
```
</details>

<details>
<summary><b>Show Target Gold Standard Reply</b></summary>

```email
Hi Maria,

I'm sorry to hear you're running into issues uploading your profile picture. We have a file size limit of 1.5MB for uploads, which is why your 2MB image is failing. 

Could you please try resizing the image to under 1.5MB and upload it again? If you continue to receive the error, please send the image file to me and I will upload it to your profile page manually.

Best,
Alex
Technical Support Team
```
</details>

---
### Test Case `test_3` - Category: `sales_inquiry`
* **Subject:** Demo request and custom integrations
* **Customer Email:** `william.brown@example.com`
* **RAG Retrieved Historical Examples:** `hist_9` (Score: 0.32), `hist_6` (Score: 0.17)

#### Scores
* **Lexical Score (Overlap):** `58.55%`
* **Semantic Score (LLM-as-a-Judge):** `77.42%`
* **Hybrid Evaluation Score:** **`69.87%`**

#### Criteria Grades
* **Factual Correctness (0-10):** `6.4` - *Simulated evaluation based on lexical overlap proxy.*
* **Tone & Professionalism (0-5):** `4.0` - *Polite sign-off and structured greeting are present.*
* **Completeness (0-5):** `4.0` - *Successfully addresses the keywords matching customer request.*
* **No Hallucination (0-5):** `5.0` - *Vocabulary stays close to the matched context templates.*

<details>
<summary><b>Show Generated Reply</b></summary>

```email
Hi William,

Thank you for your interest! Yes, we have full support for custom webhooks, which you can set up under Developer Settings.

I would be delighted to host a demo of our analytics and webhooks. You can book a suitable time via our demo link: calendly.com/demolink.

Best,
Liam
Sales Team
```
</details>

<details>
<summary><b>Show Target Gold Standard Reply</b></summary>

```email
Hi William,

Thank you for your interest! Yes, our platform supports custom webhooks, which can be configured directly from the developer console.

I would love to walk you through our reports dashboard and custom webhook setups. You can book a slot for a live demo with our team using this link: calendly.com/demolink. 

Let us know if none of those slots work, and we can find another time.

Best,
Liam
Sales Team
```
</details>

---
### Test Case `test_4` - Category: `shipping_delivery`
* **Subject:** Change shipping address for Order 7721
* **Customer Email:** `sarah.connor@example.com`
* **RAG Retrieved Historical Examples:** `hist_13` (Score: 0.46), `hist_12` (Score: 0.15)

#### Scores
* **Lexical Score (Overlap):** `74.12%`
* **Semantic Score (LLM-as-a-Judge):** `91.65%`
* **Hybrid Evaluation Score:** **`84.64%`**

#### Criteria Grades
* **Factual Correctness (0-10):** `7.9` - *Simulated evaluation based on lexical overlap proxy.*
* **Tone & Professionalism (0-5):** `5.0` - *Polite sign-off and structured greeting are present.*
* **Completeness (0-5):** `5.0` - *Successfully addresses the keywords matching customer request.*
* **No Hallucination (0-5):** `5.0` - *Vocabulary stays close to the matched context templates.*

<details>
<summary><b>Show Generated Reply</b></summary>

```email
Hi Sarah,

I have successfully updated the delivery address for Order #7721 to your home address:
789 Pine Rd
Seattle, WA 98101

Your package is still in our warehouse and will ship out to this address tomorrow. You will receive a tracking link via email soon.

Best,
Oliver
Logistics & Shipping Team
```
</details>

<details>
<summary><b>Show Target Gold Standard Reply</b></summary>

```email
Hi Sarah,

I have successfully updated your shipping address for Order #7721 to:
789 Pine Rd
Seattle, WA 98101

Your order is currently processing and will ship to this new address. You will receive a shipping confirmation email with tracking details shortly.

Best,
Oliver
Logistics & Shipping Team
```
</details>

---
### Test Case `test_5` - Category: `feature_request`
* **Subject:** Integrate with Microsoft Teams
* **Customer Email:** `daniel.craig@example.com`
* **RAG Retrieved Historical Examples:** `hist_9` (Score: 0.28), `hist_14` (Score: 0.15)

#### Scores
* **Lexical Score (Overlap):** `77.1%`
* **Semantic Score (LLM-as-a-Judge):** `92.84%`
* **Hybrid Evaluation Score:** **`86.54%`**

#### Criteria Grades
* **Factual Correctness (0-10):** `8.2` - *Simulated evaluation based on lexical overlap proxy.*
* **Tone & Professionalism (0-5):** `5.0` - *Polite sign-off and structured greeting are present.*
* **Completeness (0-5):** `5.0` - *Successfully addresses the keywords matching customer request.*
* **No Hallucination (0-5):** `5.0` - *Vocabulary stays close to the matched context templates.*

<details>
<summary><b>Show Generated Reply</b></summary>

```email
Hi Daniel,

Thanks for reaching out. We do not support native Microsoft Teams alerts directly yet, but you can easily bridge notifications using our outgoing webhooks or via Zapier.

I have registered this request with our product roadmap team, as we plan to release native Teams integration in Q3. I'll let you know as soon as it's available.

Best,
Chloe
Product Feedback Team
```
</details>

<details>
<summary><b>Show Target Gold Standard Reply</b></summary>

```email
Hi Daniel,

Thank you for reaching out! While we do not have a native Microsoft Teams integration built-in yet, you can set up notifications using our custom outgoing webhooks or via Zapier.

I have logged your request for a native Microsoft Teams integration with our engineering team, as this is on our product roadmap for Q3. I will update you as soon as it is released.

Best,
Chloe
Product Feedback Team
```
</details>

---
