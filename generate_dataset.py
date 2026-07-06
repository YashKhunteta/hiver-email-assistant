import os
import json

# Define the historical customer support database (20 items)
SUPPORT_DATASET = [
    {
        "id": "hist_1",
        "category": "billing_refund",
        "subject": "Refund for defective widget",
        "customer_email": "john.doe@example.com",
        "incoming_body": "Hello, I purchased your widget yesterday and it keeps crashing on startup. This is unusable. I would like a full refund. Order ID is #9981.",
        "historical_reply": "Hello John,\n\nI am sorry to hear that the widget is crashing on startup. I have processed a full refund of your purchase for Order #9981. You should see the funds back in your account within 5-10 business days.\n\nLet me know if you need help with anything else!\n\nBest regards,\nSarah\nCustomer Support Team",
        "meta": {"urgency": "high", "sentiment": "negative"}
    },
    {
        "id": "hist_2",
        "category": "billing_refund",
        "subject": "Duplicate charges on card",
        "customer_email": "alice.williams@example.com",
        "incoming_body": "Hi there, I noticed that I was charged twice on my credit card for the monthly subscription this month. Can you please check and refund one of them? Thanks.",
        "historical_reply": "Hi Alice,\n\nThanks for reaching out. I looked into your billing history and verified that you were double-charged due to a temporary billing sync issue. I have refunded the duplicate charge of $15.00 back to your credit card. \n\nPlease allow 3-5 business days for it to appear on your statement. I apologize for the inconvenience.\n\nWarmly,\nSarah\nCustomer Support Team",
        "meta": {"urgency": "medium", "sentiment": "neutral"}
    },
    {
        "id": "hist_3",
        "category": "account_cancellation",
        "subject": "Cancel my account subscription",
        "customer_email": "bob.smith@example.com",
        "incoming_body": "Hi support, please cancel my pro subscription immediately. I do not need it anymore.",
        "historical_reply": "Hi Bob,\n\nI have cancelled your Pro subscription as requested. Your account has been downgraded to the Free tier, and you will not be charged again. You will still have access to the Pro features until the end of your current billing cycle on July 25th.\n\nIf you ever decide to come back, we'd love to have you!\n\nBest regards,\nMark\nCustomer Retention Team",
        "meta": {"urgency": "medium", "sentiment": "neutral"}
    },
    {
        "id": "hist_4",
        "category": "account_cancellation",
        "subject": "Cancel trial account",
        "customer_email": "clara.jones@example.com",
        "incoming_body": "Hello, my trial is ending tomorrow and I want to make sure I'm not billed. Please cancel my account subscription. Thanks.",
        "historical_reply": "Hello Clara,\n\nI have cancelled your trial subscription. Your account is now set to the Free tier, and you will not be charged. If you decide to upgrade in the future, your settings and data will still be saved.\n\nHave a great day!\n\nBest regards,\nMark\nCustomer Retention Team",
        "meta": {"urgency": "high", "sentiment": "neutral"}
    },
    {
        "id": "hist_5",
        "category": "technical_bug",
        "subject": "Verification code not arriving",
        "customer_email": "david.lee@example.com",
        "incoming_body": "I'm trying to log in but the 2FA verification code is not showing up in my inbox. I checked my spam folder too.",
        "historical_reply": "Hi David,\n\nI'm sorry you are experiencing issues logging in. We had a brief delay with our email delivery partner which has now been resolved. I have manually triggered a fresh 2FA verification code to your email. Please try logging in again. \n\nIf it still does not arrive, please let us know and we can temporarily disable 2FA to get you logged in.\n\nBest,\nAlex\nTechnical Support Team",
        "meta": {"urgency": "high", "sentiment": "frustrated"}
    },
    {
        "id": "hist_6",
        "category": "technical_bug",
        "subject": "Dashboard 500 internal server error",
        "customer_email": "emma.davis@example.com",
        "incoming_body": "Whenever I click on the analytics dashboard, the page goes blank and I see a 500 Internal Server Error page. Please help, we need this report for a meeting.",
        "historical_reply": "Hi Emma,\n\nI apologize for the disruption this is causing. Our engineering team identified an issue with data indexing on the dashboard and has deployed a fix. \n\nCould you please clear your browser cache and try accessing the dashboard again? It should load correctly now. Please let me know if the error persists.\n\nBest,\nAlex\nTechnical Support Team",
        "meta": {"urgency": "high", "sentiment": "negative"}
    },
    {
        "id": "hist_7",
        "category": "technical_bug",
        "subject": "Notifications not sending out",
        "customer_email": "frank.miller@example.com",
        "incoming_body": "None of our customers are receiving order confirmation emails since yesterday. Is there a bug? This is hurting our sales.",
        "historical_reply": "Hi Frank,\n\nThank you for alerting us. We investigated and found that the API webhook for your order confirmation event was disabled in your developer settings. I have re-enabled it, and test emails are now sending correctly. \n\nCould you please check your dashboard to verify that order confirmation emails are now delivering? Let me know if you need help resending yesterday's missed emails.\n\nBest,\nAlex\nTechnical Support Team",
        "meta": {"urgency": "high", "sentiment": "negative"}
    },
    {
        "id": "hist_8",
        "category": "sales_inquiry",
        "subject": "Pricing questions for 50 seats",
        "customer_email": "grace.taylor@example.com",
        "incoming_body": "Hi, we are looking to purchase 50 seats of your software. Do you offer bulk discounts or enterprise contracts?",
        "historical_reply": "Hi Grace,\n\nThanks for your interest in our product! Yes, we absolutely offer volume discounts for teams of 50 or more. Our Enterprise plan includes custom SLAs, dedicated support, and advanced security.\n\nI have copied our Sales Executive, David (david.sales@example.com), who will reach out shortly to discuss pricing details and set up a demo for you.\n\nBest,\nLiam\nSales Team",
        "meta": {"urgency": "medium", "sentiment": "positive"}
    },
    {
        "id": "hist_9",
        "category": "sales_inquiry",
        "subject": "Integration options and demo",
        "customer_email": "henry.wilson@example.com",
        "incoming_body": "Hello, we are evaluating your app and want to know if it integrates with Slack and Jira. Can we schedule a demo this week?",
        "historical_reply": "Hi Henry,\n\nThank you for reaching out! Yes, we have native integrations with both Slack and Jira. You can set them up easily via the Integrations page in your settings.\n\nI would be happy to schedule a demo to walk you through these integrations. Please use this calendar link to book a time that works for you: calendly.com/demolink\n\nLooking forward to speaking with you!\n\nBest,\nLiam\nSales Team",
        "meta": {"urgency": "medium", "sentiment": "neutral"}
    },
    {
        "id": "hist_10",
        "category": "sales_inquiry",
        "subject": "Startup discount eligibility",
        "customer_email": "ivy.thomas@example.com",
        "incoming_body": "Hi sales team, we are a small pre-seed startup. Do you have any discounts or special pricing for early-stage companies?",
        "historical_reply": "Hi Ivy,\n\nThanks for reaching out! Yes, we run a Startup Program that offers 50% off all plans for your first year. To qualify, you just need to have raised under $2M and be less than 3 years old.\n\nYou can apply directly here: example.com/startups. Once approved, the discount will be applied to your billing portal automatically.\n\nBest of luck with your startup!\n\nBest,\nLiam\nSales Team",
        "meta": {"urgency": "medium", "sentiment": "positive"}
    },
    {
        "id": "hist_11",
        "category": "shipping_delivery",
        "subject": "Order marked delivered but not received",
        "customer_email": "jack.white@example.com",
        "incoming_body": "My package (Tracking ID: TRK8872) was marked as delivered today, but I looked everywhere and it is not here. Can you help?",
        "historical_reply": "Hi Jack,\n\nI'm sorry to hear your package hasn't arrived. Sometimes shipping carriers mark items as delivered a day early by mistake, or it may have been left with a neighbor or building manager. \n\nI recommend waiting 24 hours, and checking nearby delivery areas. If it still doesn't show up, let us know and we will file a claim with the carrier and send a replacement order.\n\nBest,\nOliver\nLogistics & Shipping Team",
        "meta": {"urgency": "medium", "sentiment": "neutral"}
    },
    {
        "id": "hist_12",
        "category": "shipping_delivery",
        "subject": "Delayed package shipment",
        "customer_email": "karen.harris@example.com",
        "incoming_body": "My order was placed a week ago and the tracking status hasn't updated from 'Processing'. When will it ship?",
        "historical_reply": "Hi Karen,\n\nI apologize for the delay. We had a brief stock shortage at our main warehouse, but your order has now been packaged and will ship tomorrow morning. \n\nOnce the carrier scans it, you will receive an automated email with tracking information. We have upgraded your shipping to Express at no extra cost as a thank you for your patience.\n\nBest,\nOliver\nLogistics & Shipping Team",
        "meta": {"urgency": "medium", "sentiment": "neutral"}
    },
    {
        "id": "hist_13",
        "category": "shipping_delivery",
        "subject": "Change shipping address",
        "customer_email": "leo.martin@example.com",
        "incoming_body": "I just placed Order #5543 but realized I entered my old apartment address. Can you please update it to 123 Main St, Apt 4B, New York, NY 10001?",
        "historical_reply": "Hi Leo,\n\nI was able to catch this before shipping. I have updated the shipping address for Order #5543 to:\n123 Main St, Apt 4B\nNew York, NY 10001\n\nYou will receive a confirmation email when it leaves our facility shortly.\n\nBest,\nOliver\nLogistics & Shipping Team",
        "meta": {"urgency": "high", "sentiment": "neutral"}
    },
    {
        "id": "hist_14",
        "category": "feature_request",
        "subject": "Does the app have dark mode?",
        "customer_email": "mia.clark@example.com",
        "incoming_body": "Hi, I love using your app but I work late at night and the bright white screen is straining my eyes. Do you have a dark mode option? If not, please add it!",
        "historical_reply": "Hi Mia,\n\nThank you for the kind words and the suggestion! Dark mode is actually one of our most requested features. \n\nI'm happy to share that our product team is actively working on it, and it's scheduled to release next month. I have added your email to our feature notifications list, so you'll receive an email as soon as it goes live!\n\nBest,\nChloe\nProduct Feedback Team",
        "meta": {"urgency": "low", "sentiment": "positive"}
    },
    {
        "id": "hist_15",
        "category": "feature_request",
        "subject": "Exporting reports to PDF and Excel",
        "customer_email": "noah.rodriguez@example.com",
        "incoming_body": "Hello, we need a way to export our analytics tables into CSV/Excel format. Right now we can only view them on the web. Is this feature coming?",
        "historical_reply": "Hi Noah,\n\nThanks for reaching out! You can actually export data to CSV directly from the page by clicking the 'Download' icon at the top right of any analytics panel. \n\nWe don't support direct PDF export yet, but we are working on it. I have shared this request with our product manager to help prioritize it. I will keep you posted on updates.\n\nBest,\nChloe\nProduct Feedback Team",
        "meta": {"urgency": "low", "sentiment": "neutral"}
    },
    {
        "id": "hist_16",
        "category": "feature_request",
        "subject": "Slack notification integrations",
        "customer_email": "olivia.lopez@example.com",
        "incoming_body": "We want our support channel in Slack to receive a ping whenever a new ticket is opened. Can we integrate your tool with Slack?",
        "historical_reply": "Hi Olivia,\n\nYes, you can easily set this up! We have a native Slack integration. To turn it on, go to Settings > Integrations > Slack, authorize your workspace, and select the channel where you want notifications posted.\n\nLet me know if you run into any issues during setup.\n\nBest,\nChloe\nProduct Feedback Team",
        "meta": {"urgency": "medium", "sentiment": "neutral"}
    },
    {
        "id": "hist_17",
        "category": "billing_refund",
        "subject": "Subscription cancellation and refund request",
        "customer_email": "paul.gonzalez@example.com",
        "incoming_body": "Hello, my subscription automatically renewed today for $30, but I meant to cancel it last week. Can you please cancel my account and refund the money? I haven't used the service today.",
        "historical_reply": "Hi Paul,\n\nI have cancelled your subscription and processed a full refund of $30.00 for today's renewal, as we have a 7-day grace period for renewals. The refund will be credited back to your original payment method in 5-10 business days.\n\nYour account has been downgraded to the Free tier. Let us know if you need any other assistance.\n\nBest regards,\nSarah\nCustomer Support Team",
        "meta": {"urgency": "high", "sentiment": "neutral"}
    },
    {
        "id": "hist_18",
        "category": "technical_bug",
        "subject": "Expired password reset links",
        "customer_email": "quinn.wilson@example.com",
        "incoming_body": "I clicked 'forgot password' but when I clicked the link in the email 5 minutes later, it said the link expired. I tried again and got the same error.",
        "historical_reply": "Hi Quinn,\n\nI apologize for the hassle. This occurs if your email client pre-scans links for security, which triggers the one-time reset token. \n\nI have generated a temporary password for you: TempPass2026!. Please use this to log in, and you will be prompted to choose a new permanent password immediately upon login. Let me know if this works.\n\nBest,\nAlex\nTechnical Support Team",
        "meta": {"urgency": "high", "sentiment": "negative"}
    },
    {
        "id": "hist_19",
        "category": "sales_inquiry",
        "subject": "HIPAA compliance questionnaire",
        "customer_email": "rachel.martinez@example.com",
        "incoming_body": "Hello, we are a healthcare clinic and need to verify if your platform is HIPAA compliant and if you will sign a Business Associate Agreement (BAA)?",
        "historical_reply": "Hi Rachel,\n\nThanks for reaching out! Yes, our platform is HIPAA compliant on our Enterprise plans. We do sign Business Associate Agreements (BAAs) for custom annual agreements.\n\nI will introduce you to our Security & Compliance officer who can provide our SOC 2 report and coordinate the BAA review. They will reach out shortly.\n\nBest,\nLiam\nSales Team",
        "meta": {"urgency": "high", "sentiment": "neutral"}
    },
    {
        "id": "hist_20",
        "category": "shipping_delivery",
        "subject": "Received damaged items",
        "customer_email": "sam.anderson@example.com",
        "incoming_body": "I received my order today, but the box was crushed and the glass flask inside was shattered. Can you send a replacement?",
        "historical_reply": "Hi Sam,\n\nI am so sorry to hear your order arrived damaged. That is definitely not the experience we want you to have.\n\nI have placed a replacement order (Order #5691-R) for the glass flask at no charge. It has been marked for expedited shipping and will ship today. You'll receive tracking information as soon as it leaves the warehouse.\n\nBest,\nOliver\nLogistics & Shipping Team",
        "meta": {"urgency": "high", "sentiment": "negative"}
    }
]

# Define separate evaluation queries (5 items)
TEST_QUERIES = [
    {
        "id": "test_1",
        "category": "billing_refund",
        "subject": "Charged for subscription after cancelling",
        "customer_email": "tom.jones@example.com",
        "incoming_body": "Hello, I cancelled my subscription two days ago, but I was charged $25 on my card this morning. Please look into this and return my money.",
        "target_reply": "Hi Tom,\n\nThanks for reaching out. I reviewed your account settings and confirmed that your cancellation did not finalize correctly before the billing run, which caused the $25.00 charge. \n\nI have finalized the cancellation of your subscription and processed a full refund of $25.00. You should see the credit on your bank statement in 5-10 business days.\n\nWe apologize for this system error and hope to welcome you back in the future.\n\nBest regards,\nSarah\nCustomer Support Team"
    },
    {
        "id": "test_2",
        "category": "technical_bug",
        "subject": "Cannot upload profile picture",
        "customer_email": "maria.gomez@example.com",
        "incoming_body": "Hi, I keep trying to upload a profile picture in JPEG format (size 2MB) but I get a red text saying 'Upload failed'. What is going wrong? Can you help?",
        "target_reply": "Hi Maria,\n\nI'm sorry to hear you're running into issues uploading your profile picture. We have a file size limit of 1.5MB for uploads, which is why your 2MB image is failing. \n\nCould you please try resizing the image to under 1.5MB and upload it again? If you continue to receive the error, please send the image file to me and I will upload it to your profile page manually.\n\nBest,\nAlex\nTechnical Support Team"
    },
    {
        "id": "test_3",
        "category": "sales_inquiry",
        "subject": "Demo request and custom integrations",
        "customer_email": "william.brown@example.com",
        "incoming_body": "Hello, we run a large logistics firm and are looking at your platform. We want to see a demo of your reports dashboard and check if you support custom webhooks. Do you have time this week?",
        "target_reply": "Hi William,\n\nThank you for your interest! Yes, our platform supports custom webhooks, which can be configured directly from the developer console.\n\nI would love to walk you through our reports dashboard and custom webhook setups. You can book a slot for a live demo with our team using this link: calendly.com/demolink. \n\nLet us know if none of those slots work, and we can find another time.\n\nBest,\nLiam\nSales Team"
    },
    {
        "id": "test_4",
        "category": "shipping_delivery",
        "subject": "Change shipping address for Order 7721",
        "customer_email": "sarah.connor@example.com",
        "incoming_body": "Hi, I ordered a toolkit ten minutes ago (Order #7721) but I realized I put the office address instead of my home address. Can you change it to 789 Pine Rd, Seattle, WA 98101?",
        "target_reply": "Hi Sarah,\n\nI have successfully updated your shipping address for Order #7721 to:\n789 Pine Rd\nSeattle, WA 98101\n\nYour order is currently processing and will ship to this new address. You will receive a shipping confirmation email with tracking details shortly.\n\nBest,\nOliver\nLogistics & Shipping Team"
    },
    {
        "id": "test_5",
        "category": "feature_request",
        "subject": "Integrate with Microsoft Teams",
        "customer_email": "daniel.craig@example.com",
        "incoming_body": "Hello, our company uses Microsoft Teams for communication. Is there an integration to send notifications from your app into our Teams channels?",
        "target_reply": "Hi Daniel,\n\nThank you for reaching out! While we do not have a native Microsoft Teams integration built-in yet, you can set up notifications using our custom outgoing webhooks or via Zapier.\n\nI have logged your request for a native Microsoft Teams integration with our engineering team, as this is on our product roadmap for Q3. I will update you as soon as it is released.\n\nBest,\nChloe\nProduct Feedback Team"
    }
]

def main():
    # Create the data directory
    os.makedirs("data", exist_ok=True)
    
    # Save the support dataset
    support_path = os.path.join("data", "support_dataset.json")
    with open(support_path, "w", encoding="utf-8") as f:
        json.dump(SUPPORT_DATASET, f, indent=2, ensure_ascii=False)
    print(f"Saved support dataset (historical database) to {support_path}")

    # Save the test queries
    test_path = os.path.join("data", "test_queries.json")
    with open(test_path, "w", encoding="utf-8") as f:
        json.dump(TEST_QUERIES, f, indent=2, ensure_ascii=False)
    print(f"Saved test dataset to {test_path}")

if __name__ == "__main__":
    main()
