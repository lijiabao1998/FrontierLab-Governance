# FrontierLab-Governance
前沿實驗室治理

## 主線
建立可追溯的計算研究流程：**先查問題是否已解 → 重現已知結果 → 凍結問題及驗證器 → 有界探索 → 獨立核查 → 記錄結果與失敗 → 審核合併。**

這個倉庫管理研究程序，不替自然界或數學決定真相。`main` 是經審核的紀錄真相源；程式通過、模型共識、業主批准，都不等於科學命題成立。

| 實驗室 | 初始題數 | 第一條主線 |
|---|---:|---|
| [FrontierMath](https://github.com/lijiabao1998/FrontierMath) | 10 | 精確構造、反例搜尋、形式證明 |
| [FrontierPhysics](https://github.com/lijiabao1998/FrontierPhysics) | 10 | 可重現模型、極限檢查、觀測約束 |
| [FrontierBiology](https://github.com/lijiabao1998/FrontierBiology) | 10 | 公開資料、跨資料集泛化、可識別性 |
| [FrontierChemistry](https://github.com/lijiabao1998/FrontierChemistry) | 10 | 基準重現、計算誤差、條件外推 |
| [FrontierComputerScience](https://github.com/lijiabao1998/FrontierComputerScience) | 10 | 可執行規格、形式驗證、系統與演算法基準 |
| [FrontierStatistics](https://github.com/lijiabao1998/FrontierStatistics) | 10 | 識別、覆蓋、錯誤率、分布偏移 |
| [FrontierMaterials](https://github.com/lijiabao1998/FrontierMaterials) | 10 | 穩定性、可合成性、跨尺度材料發現 |
| [FrontierAstronomy](https://github.com/lijiabao1998/FrontierAstronomy) | 10 | 多信使、宇宙學、早期天體與系外行星 |
| [FrontierEarth](https://github.com/lijiabao1998/FrontierEarth) | 10 | 氣候、地震、火山、海洋與地球觀測 |
| [FrontierNeuroscience](https://github.com/lijiabao1998/FrontierNeuroscience) | 10 | 腦—行為模型、表徵、動力學與因果擾動 |
| [FrontierEconomics](https://github.com/lijiabao1998/FrontierEconomics) | 10 | 生產力、企業、勞動、AI擴散與識別 |
| [FrontierEngineering](https://github.com/lijiabao1998/FrontierEngineering) | 10 | 控制、數位孿生、韌性與跨域泛化 |
| [FrontierMedicine](https://github.com/lijiabao1998/FrontierMedicine) | 10 | 外部驗證、臨床效用、試驗與監測 |
| [FrontierSocialScience](https://github.com/lijiabao1998/FrontierSocialScience) | 10 | 網路、遷移、資訊擴散與因果設計 |
| [FrontierMetaScience](https://github.com/lijiabao1998/FrontierMetaScience) | 10 | 重現性、同行評審、AI科學與研究治理 |

## 開始前必讀
1. [AGENTS.md](AGENTS.md)：角色、分支、合併與停止規則。
2. [RESEARCH_PROTOCOL.md](RESEARCH_PROTOCOL.md)：每輪檢索及完成判定。
3. [EVIDENCE_POLICY.md](EVIDENCE_POLICY.md)：證據、來源、驗證器與宣稱邊界。
4. [SAFETY.md](SAFETY.md)：公開資料、安全與預算。

## 可執行入口
Python 3.11+，僅標準函式庫。問題ID目前支援 MATH/PHYS/BIO/CHEM/CS/STAT/MAT/ASTRO/EARTH/NEURO/ECON/ENG/MED/SOC/META。先把本治理倉庫放在研究倉庫旁邊，並 checkout 研究倉庫 `GOVERNANCE.lock.json` 記錄的 commit。

```bash
python3 -m unittest discover -s tests -v
python3 tools/frontier.py validate ../FrontierMath
python3 tools/frontier.py start ../FrontierMath MATH-001 --agent gpt
# 由有聯網能力的 agent 真正搜尋、閱讀原文並填寫生成的 round.json。
python3 tools/frontier.py admit ../FrontierMath ../FrontierMath/runs/<round-id>/round.json
```

`start` 只建立 DRAFT，不搜尋、不批准實驗。`admit` 沒有完整檢索紀錄就拒絕；發現同範圍的已確認外部解答，會寫 `COMPLETED_EXTERNAL` 並停止該題探索，等待合併審查。

## 多 agent 最小配置
同一題：Explorer 提候選，Verifier 重做驗證，Skeptic 找反例與過度宣稱，Integrator 整理 PR；業主裁決資源與是否合併。角色可以跨輪輪換，但同一輪不能由作者自我簽署獨立驗證。單 agent 可做基線，不得宣稱獨立重現。

不預設五科同時燒算力。每科先以一題重現基線，其餘排隊。分支只做一個問題的一個小目標。

## 狀態不混用
- 問題：`OPEN / PARTIAL / CLAIMED_RESOLVED / COMPLETED_EXTERNAL / COMPLETED_INTERNAL / PAUSED / RETRACTED`。
- 輪次：`DRAFT / ADMITTED / PAUSED / CLOSED_EXTERNAL / FINISHED`。
- 證據另記：形式證明、精確有限證書、數值結果、統計支持、實驗支持、獨立重現。不是一條跨學科的高低排名。

`OPEN` 的意思是「本次有界檢索未找到同範圍的已確認解答」，不是證明全世界無人解出。初始題卡只是選題篩查，不替代任何新輪次的檢索。

## CI 的能力與限制
各科使用固定 commit 的共用 workflow，核對 10 張題卡、狀態和研究變更對應的輪次紀錄；治理倉庫自己測試 gate。CI 不會自動全網搜尋，也不能判定來源是否被誠實閱讀。這些要由研究者及審核者核實。

沒有配置 agent API 金鑰、常駐研究工作者或付費運算；推送只會觸發有限 CI。`CODEOWNERS` 與流程文件不等於已啟用 GitHub 分支保護；伺服器端 required reviews/checks 必須由業主另行設定。

2026-09-27：依業主本次明確指令初始化五庫。之後一律使用分支與 PR；不把本次初始化權限延伸為永久直接改 main 權限。
