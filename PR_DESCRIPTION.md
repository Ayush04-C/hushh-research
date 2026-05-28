# Description

Integrates a new **Macro-Economic Agent** into the Kai Debate Engine. This agent performs top-down macroeconomic analysis, evaluating factors such as inflation, interest rate impacts, and broad sector trends to balance out the existing fundamental, sentiment, and valuation agents. 

Specific changes include:
* **Engine Integration:** Updated `debate_engine.py` to incorporate the Macro Agent's vote into the `_calculate_weighted_decision` and `_build_consensus` methods.
* **Dynamic Weighting:** Adjusted the `AGENT_WEIGHTS` in `config.py` so the Macro Agent's influence scales depending on the user's selected Risk Profile (e.g., highly weighted for conservative profiles).
* **Streaming Fixes:** Updated the `analyze_stream_generator` in `stream.py` to cleanly yield the macro insight and pass it down into the final consensus builder without causing backend timeouts.

## 📌 Impact Map (Required)

- Routes touched:
  - [ ] None
  - [x] Listed below:
    - `/api/kai/analyze/run/start`
    - `/api/kai/agent/chat/stream`

- API / schema / type changes:
  - [ ] None
  - [x] Listed below:
    - Added `MacroInsight` dataclass.
    - Updated `DecisionResult` / `agent_votes` payload to natively support the `"macro"` key.

- Cache keys touched:
  - [x] None
  - [ ] Listed below:

- World-model domain summary effects:
  - [x] None
  - [ ] Listed below:

- Mobile parity impacts:
  - [x] None
  - [ ] Listed below:

- Docs updated (exact files):
  - [x] None
  - [ ] Listed below:

- Verification commands executed:
  - [ ] `cd hushh-webapp && npm run typecheck`
  - [ ] `cd hushh-webapp && npm test`
  - [ ] `cd hushh-webapp && npm run build`
  - [ ] `cd hushh-webapp && npm run ios:test`
  - [ ] `python scripts/ops/kai-system-audit.py --api-base http://localhost:8000 --web-base http://localhost:3000`

## 🛑 Tri-Flow Architecture Check

_Every feature must be implemented across all three layers or explicitly marked as not applicable._

- [x] **Web**: Next.js implementation (`app/api/...`) & Python backend services.
- [ ] **iOS**: Swift Capacitor Plugin (`ios/App/App/Plugins/...`) *(N/A)*
- [ ] **Android**: Kotlin Capacitor Plugin (`android/app/.../plugins/...`) *(N/A)*

## 🧪 Testing

- [x] Tested on Web (Chrome/Safari)
- [ ] Tested on iOS Simulator/Device
- [ ] Tested on Android Emulator/Device
- [x] Commits are signed off (`git commit -s`)

## 📸 Screenshots / Video

_Attach proof of work here._

*(Attach a screenshot of the detailed view here showing the 4 bars on the agent votes chart including the new Macro vote)*

## 🛡️ Privacy & Consent

- [x] Does this change access user data?
- [x] If yes, have you implemented `checkConsentToken()`? *(Passed down natively via `HushhContext` in the Debate Engine)*

## 📜 Licensing

- [x] First-party changes remain Apache-2.0 compatible
- [x] Third-party notice impact reviewed when dependencies changed
