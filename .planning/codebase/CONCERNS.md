# Current Concerns

## Technical Debt
- **Coverage Gaps:** `models/prompt.py` has low coverage on internal validation functions.
- **Firebase Emulator:** Environment lacks Java, preventing the use of local emulators. Tests depend on real Firebase connections (mitigated by VCR).
- **VCR Maintenance:** Cassettes must be manually re-recorded whenever Gemini models or prompt templates change.

## Roadmap Risks
- **Rate Limits:** Gemini free-tier quota can be reached during intensive testing if VCR is not used correctly.
- **Dependency Versioning:** `google-genai` and other SDKs are evolving fast; breaking changes may occur.

## Proposed Improvements
- Implement unit tests for `models/prompt.py` pure functions.
- Add mock handlers for Firebase to enable offline testing without VCR where appropriate.
