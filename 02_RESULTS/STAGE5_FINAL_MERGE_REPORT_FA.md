# گزارش نهایی Stage 5 — v13 FINAL10

## وضعیت اجرا
- پروتکل: v13-FINAL10-2.0-AUDITED
- Final test: 50 seed ثابت، 970001 تا 970050
- Adaptive stopping: خاموش
- B6 منتخب: 2×25، time limit=5s، MIP gap=0.05
- B6 final timeouts: 0
- B6 final fallbacks: 0
- Training stability gate: 4/5 seed پشتیبانی شد

## نتیجه اصلی خانواده پنج PPO
- میانگین هزینه PPO family: 5.6100965
- میانگین هزینه B6: 5.6519398
- اختلاف مطلق PPO-B6: -0.0418433
- CI 95% اختلاف مطلق: [-0.1734326, 0.0875511]
- میانگین کاهش نسبی زوجی: 0.3248733%
- CI 95% کاهش نسبی: [-2.1310812%, 2.8023116%]
- sign-flip p-value: 0.53649
- seedهای بهتر برای PPO family: 27/50
- اختلاف completion: +0.2226 واحد درصد
- CI completion: [-0.9186, 1.4262]

تعبیر: نتیجه خانواده پنج PPO از نظر جهت به نفع PPO است، اما از نظر آماری قطعی نیست و نباید به‌عنوان برتری تأییدشده نسبت به B6 گزارش شود.

## Deployment policy از پیش انتخاب‌شده
- training seed منتخب: 1004
- مبنای انتخاب: minimum selected development robust score؛ tie با median و سپس seed id
- میانگین هزینه: 5.2272905
- اختلاف مطلق PPO-B6: -0.4246494
- CI 95%: [-0.5739745, -0.2797055]
- میانگین کاهش نسبی زوجی: 6.9917284%
- CI 95%: [4.4832217%, 9.5131277%]
- sign-flip p-value: 0.0000199996
- seedهای بهتر: 39/50
- اختلاف completion: +2.9787 واحد درصد
- CI completion: [1.7731, 4.2413]

تعبیر: policy قابل استقرار که فقط با development انتخاب شده، روی Final Test تازه عملکرد بهتر و CI کاملاً جدا از صفر دارد. این نتیجه برای framing deployment قابل دفاع است، به شرط اینکه در مقاله به‌وضوح secondary/deployment estimand و قاعده انتخاب development-only توضیح داده شود و جای نتیجه primary family mean جا زده نشود.

## پراکندگی بین training seedها
- Seed 1001: بدتر از B6، اختلاف +0.2144، CI مثبت
- Seed 1002: بهتر از B6، اختلاف -0.5148، CI منفی
- Seed 1003: بدتر از B6، اختلاف +0.2808، CI مثبت
- Seed 1004: بهتر از B6، اختلاف -0.4246، CI منفی
- Seed 1005: بدتر از B6، اختلاف +0.2350، CI مثبت

این پراکندگی نشان می‌دهد training variability مادی است. به همین دلیل hierarchical bootstrap نیز گزارش شده و CI آن برای family effect برابر [-0.3830, 0.2775] است.

## تجزیه اختلاف هزینه family PPO-B6
- service: -0.1200233
- switch: +0.0061067
- recovery: -0.0016210
- restart: تقریباً صفر
- tardiness: -0.0249955
- terminal: +0.0986881

کاهش service و tardiness به نفع PPO است، ولی terminal بالاتر بخشی از مزیت را خنثی می‌کند.

## نتیجه علمی برای مقاله
1. عدد تاریخی 7.40% S14 نباید حفظ شود.
2. primary family-of-five result باید به‌عنوان نتیجه نامطمئن/غیرقطعی گزارش شود.
3. deployment policy seed 1004 که فقط با development انتخاب شده، نتیجه قوی و قابل دفاعی دارد و باید به‌عنوان نتیجه deployment secondary برجسته شود.
4. variability بین training runs باید در Discussion و Limitations صریح باشد.
5. ادعای convergence مطرح نشود؛ فقط training stability diagnostics گزارش شوند.
6. نمودارهای validation trajectory، entropy/KL، B6 selection، paired cost، robustness forest، completion و decomposition آماده‌اند.
