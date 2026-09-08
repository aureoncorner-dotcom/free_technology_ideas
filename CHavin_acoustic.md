# Chavín acoustic source-recovery packet
CC) - NO RIGHTS RESERVED
8 September 2026 · v0.1 · Author: Anonymous · Newly authored text and intake templates: CC0 1.0

**Status: source audit completed; dimension-matched transmission comparison `NOT_RUN`; archaeological conclusion unchanged.**

The corpus contains the executable ideal-duct baseline, its results and integrity records, the stress-test narrative, and a later empirical-input audit. It contains useful published measurement descriptions and numerical summaries. This pass did not recover the joined, calibrated central/north/south duct recordings, verified interior geometry, and matched controls needed for the stronger comparison. “Not recovered” describes this search; it does not establish that the records do not exist.

This is a separate recovery packet. The original reports, baseline archive, bands, score, and published findings remain as recorded. Third-party publications and survey data retain their own rights; the CC0 statement applies to new packet text and templates only.

## 1. What already exists in the corpus

| ID | Recovered item | What it establishes | What it does not supply |
|---|---|---|---|
| C01 | [September 8 stress-test Drive record](https://docs.google.com/document/d/1I_bpAt7J6NF6FgpYDTibkAnjNaTGrfDofVBVXk8ExaA/edit?usp=drivesdk) | v1.0 narrative, analytical result, and section 5 empirical specification. Observed modified time: 2026-09-08 02:47:04.385 UTC. | Raw acoustic or survey files. |
| C02 | `Chavin_Acoustic_Stress_Test_2026-09-08.md` · 11,928 bytes | Saved narrative; byte-identical to the narrative inside C03. | A new measurement or independent replication. |
| C03 | `Chavin_Duct_Test_2026-09-08.zip` · 124,187 bytes | Original code, protocol, results, figure, README and checksum manifest. | A pressure-transfer simulation or empirical duct dataset. |
| C04 | `Chavin_empirical_input_audit.md` · 10,934 bytes | Prior recovery findings, source distinctions, exact leads and `NOT_RUN` decision. | The underlying raw files described by those sources. |
| C05 | [Geometry review, later September 8 copy](https://docs.google.com/document/d/11nOlChBSZwKD8xm-mu6uQ-JFVYPdLkSK8nL1_9yJGXk/edit?usp=drivesdk) | Its Chavín entry carries forward the weak-match result and proposed stronger test. | An additional data recovery. |

The accompanying ZIP preserves C02–C04 as exact copies in `corpus/`. C01 and C05 are linked native records; they were read, not modified. Their native Google Docs bytes are not claimed to have been exported or hashed.

**C03 integrity check:** all eight entries in its existing checksum manifest match. The result file’s code and protocol hashes match the archived code and protocol. `coverage.csv` contains 144 data rows; `bandwidth_controls.csv` contains 128. The archived five-item validation receipt was inspected. The numerical experiment was not rerun in this recovery pass.

The archive’s nine members are the narrative, `README.md`, `SHA256SUMS.txt`, `duct_baseline.py`, `protocol.json`, and four results files: `coverage.csv`, `bandwidth_controls.csv`, `results.json`, and `duct_controls.png`. There are no recording or duct-mesh members. The PNG is a synthetic baseline figure.

## 2. Requirements mapped to recovered evidence and remaining work

“Corpus record” means a source description or finding is already saved. “Publicly verified” means the cited source was inspected again in this pass. Neither status means the underlying empirical data are in hand.

| ID / required input | Already recorded in the corpus; fresh public check | Still required for the specified test | Recovery route / present fitness |
|---|---|---|---|
| R01 · Excitation and input/output recordings | C01/C04 identify [2012 Figure 13](https://culturalacoustics.org/publications/KolarEtAl2012_IntegrativeArchaeoacousticsPututus_Chavin.pdf), freshly inspected. It provides plotted responses. | Original excitation and synchronized pressure-reference/output channels, all runs, channel map and processing lineage; or a demonstrably equivalent auditable raw package. | Q01. Published figure available; raw package unrecovered. |
| R02 · Calibration, processing and noise | C04 identifies the distinction between a plotted response and a traceable pressure ratio. | Source/microphone response records, gains, calibration dates and units, timing alignment, deconvolution settings, noise/background recordings and clipping checks. | Q01. No complete duct-run calibration chain recovered. Instrument or playback calibration is a different measurement context. |
| R03 · Source/receiver positions | The [2012 methods, printed p. 41](https://culturalacoustics.org/publications/KolarEtAl2012_IntegrativeArchaeoacousticsPututus_Chavin.pdf) document an MM-4XP at interior openings and four B6 microphones near duct ends. | Run-linked coordinates, orientation, aperture offsets, position uncertainty, coordinate frame, and mapping to the surveyed duct. | Q01 + Q03. Partial documentation; precise metadata unrecovered. |
| R04 · Repeats | [Figure 13 and its caption](https://culturalacoustics.org/publications/KolarEtAl2012_IntegrativeArchaeoacousticsPututus_Chavin.pdf) show three consecutive tests per duct. | Separate repeat files and IDs, run order, exclusions, and a record of which repeats used unchanged placement versus repositioning. | Q01. Repetition reported; original trials and placement variation unrecovered. |
| R05 · Instrument spectra | C04 records results now rechecked in [Cook et al. 2010, Tables 2–3](https://ccrma.stanford.edu/groups/chavin/publications/ASA2010_ChavinPututus.pdf): played-frequency summaries, distinct bore peaks and hole conditions. | Individual source recordings/spectra with calibration, instrument and take IDs, excitation type, hole/hand state, and independently specified band definitions. | Q02. Numerical summaries available; complete calibrated spectra unrecovered. |
| R06 · Temperatures and environment | C04’s 16 °C / 41% RH entry is confirmed in the [2012 outdoor echo experiment, pp. 35–36](https://culturalacoustics.org/publications/KolarEtAl2012_IntegrativeArchaeoacousticsPututus_Chavin.pdf). | Conditions recorded for each duct session, location/time, uncertainty and environmental variation. | Q01. Existing value has the wrong measurement context and cannot fill the duct-temperature field. |
| R07 · 3D duct and connected-space geometry | C01 records approximate endpoints/lengths. [Open Heritage 3D](https://openheritage3d.org/project.php?id=w54r-pb82) and [ArcTron](https://www.arctron.de/references/2012-en/chavin-peru/) are verified survey leads. | Observed central/north/south interior coverage, cross-sections along the path, bends, apertures, connected volumes, surface/boundary information and reconstruction uncertainty, registered to the acoustic session. | Q03. Endpoint dimensions are partial geometry; complete interior coverage is unverified. |
| R08 · Dimension-matched ordinary controls | C03 supplies ideal uniform-duct frequency controls. C04 notes other gallery/canal measurements. | Identified ordinary-duct geometry/transfer pairs and a declared matching rule; explicit length/volume/profile/source-placement constraints for each comparison or ablation. | Q03 and follow-on control acquisition. No qualifying ordinary-control dataset recovered. Side ducts provide a within-site contrast, not automatically ordinary matched controls. |
| R09 · Held-out validation and model authority | C01 §5 requires validation; C03 validates only its ideal frequency calculation. | A versioned reconstruction, measured data reserved from fitting/tuning, boundary/loading assumptions and an independently evaluated validation result. | After R01–R08 recovery. No empirical model-validation result exists in the recovered package. |

**Existing dimension summary:** C01/C02 preserve an approximately 4.5 m central duct, inlet 0.33 × 0.40 m, outlet 0.12 × 0.085 m, and approximately 7 m preserved side ducts. These are reported dimensions, not a recovered internal profile or a new survey.

**Instrument distinction to preserve:** Strombus 4’s played overtone is 565.52 Hz (SD 7.36); its separate bore peaks F2 and F3 are 575.68 and 826.17 Hz. These are different measured quantities. A frequency SD is not a spectral bandwidth. The frozen aggregate bands below are not replaced by these values. The 2010 paper also describes recorded calibration sweeps; the raw sweeps remain a retrieval target. [Cook et al., pp. 3–4 and 7–8](https://ccrma.stanford.edu/groups/chavin/publications/ASA2010_ChavinPututus.pdf).

## 3. Named public leads: fresh verification

| ID / source | Verification in this pass | Exact remaining target |
|---|---|---|
| P01 · [Kolar et al. 2012 author PDF](https://culturalacoustics.org/publications/KolarEtAl2012_IntegrativeArchaeoacousticsPututus_Chavin.pdf) | Full PDF retrieved; Figure 13 visually checked; methods and environmental context read. | Figure 13’s original recording and processing package, connected to its three named ducts. |
| P02 · [Cook et al. 2010, Stanford PDF](https://ccrma.stanford.edu/groups/chavin/publications/ASA2010_ChavinPututus.pdf) | Full PDF retrieved directly; Tables 2–3 visually checked and acquisition/calibration methods read. | 2008 instrument takes, calibration sweeps, trial metadata and complete spectra. |
| P03 · [Kolar 2013 dissertation record](https://purl.stanford.edu/yn767xd4431) | Landing page, public manifest and 221-page PDF inspected. The manifest exposes the dissertation PDF; that PDF contains zero embedded files. | Printed p. 41 / PDF page 54 identifies Strombus 2 “Cupisnique,” September 2008, “Take 10, Mic 4.” Recover the original recording and its context. A localization-study stimulus is not a duct input/output pair. |
| P04 · [Kolar, Ko and Kim 2021](https://www.mdpi.com/2624-599X/3/1/12) | Publisher full text inspected. Tables 3–4 concern Laberintos/Rocas metrics and a Lanzón broadband level map. The historical data statement anticipated an IR release in 2022 and a corresponding-author request route. | Present accession/file list and measurement-to-location mapping. The historical availability statement is not a current embargo finding. Reduced room metrics and broadband levels cannot reconstruct the required frequency-dependent pressure ratio. |
| P05 · [Aural Heritage 2023 white paper](https://auralheritage.org/publications/NEH_GrantPR-263931-19_AuralHeritage_WhitePaper2023.pdf) | Public report inspected; pp. 2 and 11 point to Belmont for case-study data. | Identify which Chavín datasets that statement covers and whether any include the older duct runs. |
| P06 · [Belmont Aural Heritage index](https://repository.belmont.edu/auralheritage/) | Current inspected index describes Chavín among three case studies but exposes collection links for Columbia Studio A and Rochester Savings Bank only. | Chavín accession, alternate deposit, unlisted collection, request-only access, or confirmation of current deposit status. Index nonappearance is not proof of non-deposit. |
| P07 · [CyArk / Open Heritage 3D, DOI 10.26301/w54r-pb82](https://openheritage3d.org/project.php?id=w54r-pb82) | Published terrestrial LiDAR listing: 49.99 GB; collected 17–24 July 2017; published 16 April 2018; license labeled CC BY-NC-SA; model described as without georeferencing. The page offers emailed data links. | Coverage inventory first: verify all three narrow interiors, registration, accuracy, occlusions and relation to the acoustic measurement date. The dataset was not acquired and no request form was submitted. A sound local coordinate frame can suffice. |
| P08 · [ArcTron’s 2012 Chavín project](https://www.arctron.de/references/2012-en/chavin-peru/) | Public project account confirms survey/reconstruction work and scanned monuments. No downloadable duct-interior model was identified on the inspected page. | Survey custodian and measured interior coverage, distinguished from display reconstructions and monument models. |
| P09 · [Aural Heritage case studies](https://auralheritage.org/sites.html) and [publications/events](https://auralheritage.org/eventspublications.html) | Both inspected; the latter includes a 2025 workshop listing. Neither inspected page supplies the required duct raw-data accession. | Routing support for Q04; demonstrations and project activity are not evidence of a deposited measurement package. |

Initial web-reader failures for P02–P04 were resolved by direct public retrieval. They are not classified as missing publications. The remaining gaps concern underlying data and fitness for this specific comparison.

## 4. Recovery requests ready for use

These are file and metadata specifications. **No message has been sent.** Published organizational channels are routing leads; custody of the specific files must be confirmed.

### Q01 · Figure 13 duct measurement package

**Target:** the study authors or measurement archive custodian for P01. The [Cultural Acoustics author site](https://culturalacoustics.org/) establishes the research lineage; the [Aural Heritage project contact](https://auralheritage.org/contact.html) can route an archive inquiry.

Please identify the original data package underlying Figure 13 of the 2012 Chavín study, with accession/version and access conditions. For each central, north and south duct configuration, supply the original excitation signal, all available recorded channels and repeat trials, and a run manifest mapping channel numbers to inlet/reference and outlet/other microphone locations. Include source and microphone settings, response/gain calibration, sample rate and timing information, background/noise records, processing or deconvolution files, and documentation of omitted or invalid trials.

Please supply session-specific positions and orientations, aperture offsets, coordinate units/frame, temperature and humidity records, and photographs or field notes identifying openings, obstructions and the site condition. State which observations were contemporaneous and which are later reconstructions. Where a requested item was never recorded, is lost, is restricted or is held elsewhere, distinguish those cases explicitly. If only processed responses survive, provide their input-reference definition and processing lineage without presenting them as raw recordings.

**Receipt needed:** R01–R04 and R06 joined by duct, session, configuration, run and channel identifiers. A digital excitation file alone does not establish the acoustic inlet pressure.

### Q02 · Per-instrument source package

**Target:** the 2008 instrument measurement archive associated with P02 and P03; use the verified project route above to identify its custodian.

Please identify the recordings underlying Tables 2–3 of Cook et al. 2010, including original multichannel takes and calibration sweeps. Preserve instrument identifiers and aliases, excitation type, hole condition, hand/bell placement, microphone mapping, trial/repeat labels, and analysis settings. The dissertation’s Strombus 2, September 2008, Take 10/Mic 4 record is one precise locator; it is not a replacement for the per-instrument collection.

Supply full spectra or the recordings needed to derive them, with frequency/amplitude units and calibration provenance. Keep played tones and impulse-excited bore responses distinct. Record unavailable, unattempted and unplayable conditions as those conditions, not as zero-valued measurements.

**Receipt needed:** R05, with any new instrument-band rule and its uncertainty specified independently of comparative duct outcomes.

### Q03 · Interior geometry and control-data inventory

**Target:** CyArk/Open Heritage 3D for P07; ArcTron for P08. [Open Heritage 3D’s public contact](https://openheritage3d.org/contactPage) lists `admin@openheritage3d.org`; [ArcTron’s project page](https://www.arctron.de/references/2012-en/chavin-peru/) links its organizational contact.

Please provide a coverage inventory before transfer of the large survey archive. Identify scan stations and files that observe the full interiors of the central, north and south Lanzón ducts, their apertures and connected spaces. Supply units, scale, coordinate transformations, registration accuracy, resolution, occlusion maps and representative cross-sections. Mark measured surfaces, interpolated gaps and reconstructed ancient fabric separately. Explain changes between survey and acoustic-session site states.

Please identify any existing ordinary-duct survey and acoustic-response pairs suitable for a dimension-matched comparison. For each candidate, provide measurement IDs and the actual geometry/response records so matching can be assessed. If no coverage exists for critical interiors, state that limitation; a new survey would be new data, not recovered historical geometry.

**Receipt needed:** R07 plus candidate R08 records. Endpoint dimensions, a monument mesh, general canal coverage and the 8 cm ideal control do not establish a matched interior model.

### Q04 · Resolve the Aural Heritage accession gap

**Target:** the [Aural Heritage project contact](https://auralheritage.org/contact.html), `admin@auralheritage.org`, and the Belmont repository route shown in P06.

The 2023 white paper directs readers to Belmont for case-study data, while the inspected collection index names Chavín but does not expose its collection. Please identify the current Chavín accession, file inventory, version, license and access route, including any alternate or unlisted deposit. Clarify the dates, galleries and experiments represented, and whether the collection contains the 2012 Figure 13 duct runs, later gallery recordings, or both. If originals are held by a different custodian, please provide that archive reference.

**Receipt needed:** a file-level mapping, not merely confirmation that Chavín was a project case study. Newly found room IRs must still be evaluated against R01–R09.

## 5. Exact intake fields and joins

The companion `recovery_register.json` contains the requirement statuses. `intake_template.json` is an unfilled handoff template; its nulls and empty arrays are not measured zeros or recovered files. These field names are proposed administrative structure for this packet, not new scientific pass thresholds.

| Record | Required fields or linked records |
|---|---|
| Asset | `asset_id`, original filename, source URL/accession/version, custodian, retrieval time, byte count, SHA-256, format, license/access terms, raw/processed/reconstruction status, and parent asset IDs for derivatives. |
| Run | `run_id`, session/configuration/repeat group, duct ID, repeat type, datetime/timezone, input/output/excitation asset IDs, channel map, calibration IDs, placement IDs, environment ID, site-state ID and processing ID. |
| Channel | Channel number and role; transducer ID/model; sensitivity/gain and units; polarity/time alignment; location/orientation; reference plane; clipping/noise assessment. |
| Placement | `placement_id`, coordinate frame/units, xyz, orientation and convention, aperture offset, uncertainty, survey registration and a run-linked diagram/photo. |
| Environment | `environment_id`, run/session linkage, timestamp, thermometer/location, temperature in °C and uncertainty, RH and uncertainty, and other recorded conditions. Missing observations remain missing. |
| Calibration / processing | Frequency-dependent source/channel response, level conversion, calibration date, gain history, sample rate, synchronization, excitation and inverse-filter files, deconvolution/windowing/smoothing choices, software/version and derived-file lineage. |
| Instrument | `instrument_id`, aliases, original/replica status, take/repeat, excitation, hole and hand states, mic/placement, calibration, spectrum units, independent band rule and uncertainty. |
| Geometry | `geometry_id`, survey date/version, raw survey and derived model assets, units/frame, each duct’s coverage, cross-section path, connected spaces, registration/resolution/occlusions, surface/boundary properties, uncertainties and measured/reconstructed labels. |
| Control / validation | `control_id`, geometry and run IDs, rationale, matched and varied quantities, matching tolerances, ablation definition, model version, loading/boundaries, fit-data IDs, held-out IDs, and a validation criterion declared before comparative results are assessed. |

**Joining rule:** each raw/processed response must resolve to its exact run, channel, placement, calibration and site state. Each geometric comparison must resolve to the relevant survey/model version and measurement configuration. Dates, filenames or the word “Chavín” alone are not sufficient joins.

**Acquisition versus new work:** raw records and field notes may be recoverable from existing archives. If calibration, positional metadata, interior coverage or ordinary controls were never recorded, those elements would require a separately documented measurement campaign or survey. The current evidence does not determine which unrecovered elements exist privately. Held-out validation and the comparison itself remain future analyses even if every source file is recovered.

## 6. Frozen analysis boundary and readiness

The reference is C01 §5 and C02, carried forward without a scoring change:

| Quantity | Frozen interval |
|---|---:|
| H1 | 272–340 Hz |
| H2 | 575–706 Hz |
| U, the source-informed upper overlap band | 826–900 Hz |

For a calibrated pressure transfer function H(f):

`G(B) = 10 log10(mean over B of |H(f)|²)`

`S = min[G(H1) − G(H2), G(U) − G(H2)]`

Preserve the pressure-reference definition and original amplitude records. This score concerns pressure ratios; it is not an acoustic-power score. A frequency-independent overall gain cancels from S, but frequency-dependent response errors do not. Absolute transmission and comparisons of levels between conditions still require their calibration records. Peak-normalizing curves does not restore missing calibration.

Plot digitization, broadband dBA, room-decay metrics, synthetic mode locations and isolated instrument peaks are not substitutions for the specified empirical input. No proxy score was calculated. Any later digitization exercise would have its own exploratory identity and would average linear squared magnitudes with appropriate frequency weighting, not average plotted dB values as if they were linear energy.

C01’s approximate central length and end sections do not define its internal profile. Its calculated area ratio is 12.94:1; the approximately 3.6:1 narrowing description is not an interchangeable area ratio. The original model also notes that the wide inlet makes a purely one-dimensional treatment of the upper band insufficient as a validated representation. No unobserved duct surfaces were filled in during this recovery pass.

Before executing the specified comparison, confirm every required join and input’s fitness, define what each ordinary control and ablation holds matched, preserve source-placement/loading differences, and validate numerical reconstruction against reserved measurements. Technical repeats estimate repeatability; they do not create independent archaeological sites.

The reference specification does not provide a numerical S acceptance cutoff, numerical matching tolerances, a complete control sampling frame, or a fixed held-out split. Those choices must be documented in a distinct execution plan before comparative outcomes are used to select them. This packet adds none of those values and does not label the post-hoc baseline as preregistered.

| Activity | Status after this packet |
|---|---|
| Existing corpus and archive integrity audit | Completed |
| Named public-source/repository check | Completed within the scope below |
| Traceable pressure-transfer scoring | `NOT_RUN` |
| Dimension-matched ordinary-control comparison | `NOT_RUN` |
| Geometry ablations and held-out empirical model validation | `NOT_RUN` |
| Archaeological conclusion | Unchanged |

The completed baseline remains a challenge to broad frequency coincidence in its tested ideal-duct family. Published selective-filtering observations remain published observations, not measurements reproduced here. Intentional design remains an archaeological interpretation requiring the stronger comparison and contextual evidence; purposeful acoustic use is not refuted. This packet adds no cross-tradition transmission evidence or historical probability estimate.

## 7. Search coverage and audit receipt

Targeted Library title searches covered Chavin, Chavín, pututu and Kolar. Content searches covered Lanzón/duct, Countryman B6, the survey DOI suffix and the precise instrument-take locator. The relevant additional title hit was the original baseline ZIP. Drive searches used Chavín/Chavin, pututu and Kolar; the stress test and geometry-review references were inspected. Gmail’s combined topic/file-identifier search returned no messages. GitHub’s `Chavin` search under `MailanPatternMonkey-ai` returned no default-branch code matches.

The public pass inspected the linked author, Stanford, publisher, Aural Heritage, Belmont, Open Heritage 3D and ArcTron sources, including the dissertation’s public file manifest. P01’s Figure 13 and P02’s Tables 2–3 were checked visually. Direct public retrieval resolved the initial reader errors for P02–P04. A rejected filtered Library query was replaced with a successful unfiltered query; the rejected request is not counted as a negative search.

This is targeted retrieval of accessible records, not a complete inventory of every unindexed attachment, unrelated archive, private institutional holding or historical Git branch. No original source was edited; no person was contacted; no data-request form was submitted; no large survey archive was acquired. The source PDFs were inspected as references and are linked rather than redistributed in the packet.

The bundle contains this report, three exact corpus files, `recovery_register.json`, `intake_template.json`, `audit_receipt.json`, and `SHA256SUMS.txt`. The receipt records full source and archive-member hashes, source locations, search scope, reference-download metadata and the verification outcomes. The new bundle manifest covers its members except itself; it does not replace the original archive manifest.
