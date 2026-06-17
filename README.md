# 자산관리 PWA

부동산·금융자산·대출을 한 화면에서 보고, 엑셀처럼 **날짜별로 금액 변동을 누적 기록**하고,
**대출이자를 자동 계산**하는 1인용 웹앱입니다. 프레임워크·빌드도구 없이 순수 HTML/CSS/Vanilla JS로
만들어졌고, GitHub Pages에 올리면 **안드로이드에 설치(PWA)되어 오프라인으로 동작**합니다.

- 데이터는 이 기기의 `localStorage`(JSON)에만 저장됩니다. 서버로 전송되지 않습니다.
- 차트는 Chart.js CDN만 사용, 그 외 의존성 없음.
- JSON 내보내기/가져오기로 백업·기기 이전 가능.

---

## 주요 기능

- **대시보드**: 순자산(증감액·증감률), 총자산/총부채, 자산 구성 도넛 차트, 순자산 추이 라인 차트, 이번 달 총 이자 부담액.
- **목록**: 카테고리별 그룹, 각 행에 현재액·직전 대비 증감·마지막 업데이트일 + [수정/기록추가/삭제].
- **날짜별 기록(시계열)**: 항목 상세에서 `날짜 | 금액 | 메모` 표를 셀 인라인 편집, 새 행 추가, 행 삭제, 날짜순 자동 정렬, 같은 날짜 덮어쓰기 확인.
- **대출이자 자동 계산**: 현재 적용금리/상환방식/만기 표시·수정, 변동금리 이력 추가, 월 이자·월 납입금(원금/이자 분리)·잔여 만기까지 총 예상 이자 계산.
- **데이터 관리**: 내보내기 / 가져오기 / 전체 초기화.

---

## 로컬에서 실행 (개발/검증)

`file://`로 열면 서비스워커가 등록되지 않으므로 **반드시 HTTP 서버로** 실행합니다.

```bash
python3 -m http.server 8000
# 브라우저에서 http://localhost:8000 열기
```

검증 체크리스트 (Chrome DevTools → Application 탭):

- 콘솔 에러 0
- **Service Workers**: `sw.js` 활성(activated and running)
- **Manifest**: `자산관리` 인식, 아이콘 3종 표시
- **Installability**: "Add to Home screen" 가능, 경고 0
- 차트 렌더, 기록 추가/수정/삭제, 이자 계산값 정상

---

## GitHub Pages 배포

1. GitHub에 저장소 생성 후, 이 디렉터리를 **루트에** push.
   ```bash
   git remote add origin https://github.com/<id>/<repo>.git
   git branch -M main
   git push -u origin main
   ```
2. 저장소 **Settings → Pages → Build and deployment → Source: Deploy from a branch**.
3. **Branch: `main` / 폴더: `/ (root)`** 선택 후 저장.
4. 잠시 후 `https://<id>.github.io/<repo>/` 에서 접속.

> **상대경로 주의**: GitHub Pages는 `/<repo>/` 하위에서 서빙되므로 모든 경로는 상대경로(`./`)입니다.
> 절대경로(`/...`)를 쓰면 아이콘·서비스워커·manifest가 404가 됩니다. (이 프로젝트는 이미 상대경로만 사용.)

---

## 안드로이드에 설치 (PWA)

1. 배포된 `https://<id>.github.io/<repo>/` 주소를 **안드로이드 Chrome**으로 엽니다.
2. 주소창 우측 **⋮ 메뉴 → "앱 설치"**(또는 자동으로 뜨는 설치 배너), 혹은 앱 상단의 **"⬇ 앱 설치"** 버튼을 탭합니다.
3. 홈 화면에 아이콘이 추가됩니다. 설치되면 WebAPK로 등록되어 **전체화면·자체 스플래시·홈 아이콘**이 생깁니다.
4. 설치 후 비행기 모드로 전환해 **오프라인 동작**을 확인하세요. (데이터가 localStorage라 완전 오프라인으로 동작합니다.)

이미 설치되어 standalone으로 실행 중이면 "앱 설치" 버튼은 자동으로 숨겨집니다.

### (선택) 진짜 APK 파일이 필요하면

플레이스토어가 아니라 직접 설치(sideload)용 APK가 필요하면, GitHub Pages 배포 후
[PWABuilder](https://www.pwabuilder.com/)에 배포 URL을 넣어 **Android 패키지(APK)** 를 생성하는 것이
가장 간단합니다. 더 세밀한 제어가 필요하면 [Bubblewrap](https://github.com/GoogleChromeLabs/bubblewrap)으로
해당 URL을 TWA(Trusted Web Activity)로 감싸 APK를 빌드할 수 있습니다. 두 방법 모두 원본 PWA를 그대로 감싸므로
품질이 좋습니다.

---

## 캐시 갱신 (배포 후 변경 반영)

서비스워커가 앱 셸을 캐시하므로, 파일을 바꿔 다시 배포할 때는 **`sw.js`의 캐시 버전을 올려야** 사용자에게 반영됩니다.

```js
// sw.js
const CACHE = 'asset-app-v1';   // → 'asset-app-v2' 로 올리고 push
```

버전을 올려 push하면 다음 방문 때 새 서비스워커가 설치되고, 앱에 **"새 버전이 있습니다 · 새로고침"** 토스트가 떠
탭하면 즉시 갱신됩니다.

---

## 아이콘 재생성

아이콘은 `tools/make-icons.py`(Pillow)로 생성합니다. 테마색 배경에 원화 기호 `₩`를 그립니다.

```bash
pip install pillow
python3 tools/make-icons.py
# → icon-192.png, icon-512.png, icon-maskable-512.png (저장소 루트)
```

maskable 아이콘은 안드로이드 어댑티브 아이콘(원/스쿼클 마스킹)에서 잘리지 않도록
심볼을 **중앙 안전영역(가운데 80%)** 안에 배치합니다.

---

## 파일 구조

```
.
├── index.html              앱 본체(UI·로직·상태관리·SW 등록)
├── manifest.webmanifest    PWA manifest
├── sw.js                   서비스워커(앱 셸 캐시 + 오프라인)
├── icon-192.png            아이콘
├── icon-512.png            아이콘
├── icon-maskable-512.png   안드로이드 maskable 아이콘
├── tools/make-icons.py     아이콘 생성 스크립트
└── README.md
```

## 데이터 백업

상단 **⤓ 내보내기**로 `자산관리-YYYY-MM-DD.json`을 저장하고, 새 기기에서 **⤒ 가져오기**로 복원합니다.
