# External Integrations

## Firebase (Google Cloud)
- **Firestore:** Main NoSQL database for users and study guides.
- **Auth:** Authentication service using identity toolkit REST API for sign-in and Admin SDK for user management.
- **Service Account:** Managed via `service-account.json`.

## Google Gemini API
- **Model Family:** Gemini (1.5, 2.5, 3.0, 3.1)
- **Features:** Content generation for study guides and input validation.
- **SDK:** `google-genai` (httpx-based).
- **Redundancy:** Implemented model cycling to handle rate limits (429/503 errors).
