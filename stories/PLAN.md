# REDAM — automatic stories (Facebook + Instagram)

Brand: Redam Travel Agency (Metricool brand id `7671028`, timezone Africa/Casablanca).
WhatsApp 060 905 06 21 · www.redamtravel.com · Contact@redamtravel.com

## Rhythm
- 2 stories per day, **10:00** and **18:00** (Africa/Casablanca) — the audience peaks per Metricool best-time data (10h is the top hour every day on FB+IG, 18h the evening peak), on `facebook` + `instagram`, type `STORY` (no text).
- 10:00 = an image story from `stories/out/` (offer poster or question). 18:00 = a vertical video ≤ 60 s.
- Media URLs are public raw GitHub links:
  `https://raw.githubusercontent.com/lamsreda-cmd/redam-media/main/<path>`

## Image stories (`stories/out/*.jpg`, made by `stories/tool/make_stories.py` from `stories/tool/stories.json`)
s_merzouga_ouarzazat, s_omra_11999, s_q_destination, s_dakhla, s_omra_istanbul, s_marrakech,
s_qods, s_ouzoud, s_omra_chaaban, s_grand_sud, s_q_teambuilding, s_omra_ramadan, s_services,
s_site, s_nos_offres, s_reservez

Date-bound offers — do NOT schedule after these dates (or edit the sub-line first):
- s_omra_11999: departures 10/11, 24/11, 22/12/2026 → drop after 2026-12-20
- s_omra_istanbul: next departure 04/12/2026 → drop after 2026-12-01
- s_qods: next departure 25/11/2026 → drop after 2026-11-22
- s_omra_chaaban: trip 17/01/2027 → drop after 2027-01-10

## Video stories (≤ 60 s, vertical)
tiktok/01_ra2y_mo3tamirin_matar.mp4, tiktok/02_ra2y_mo3tamirin_makka.mp4, tiktok/03_ra2y_mosafirin_1.mp4,
tiktok/04_ra2y_mosafirin_2.mp4, tiktok/05_ra2y_mosafira_3.mp4, tiktok/06_3ard_dakhla.mp4,
tiktok/07_3ard_imlil_agafay.mp4, tiktok/08_3ard_merzouga.mp4,
tiktok/09_wach_3arf_nasa2ih.mp4 (AI presenter → instagramData.isAiGenerated = true),
videos/redam_istanbul_ugc_v3.mp4, videos/redam_tunisie_ugc_v4.mp4, videos/redam_toutes_nos_offres_v4.mp4
Any new vertical video ≤ 60 s added under `videos/` joins the rotation.

## Rules
- Rotate so the same item is not repeated within 7 days; alternate offers / testimonials / questions.
- Never invent prices, dates or seat counts. Only use what is in the files.
- Never write "الكار" — write "نقل سياحي مكيّف".
- The first batch covers 2026-10-29 → 2026-11-11.
