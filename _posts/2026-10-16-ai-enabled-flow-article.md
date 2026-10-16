---
title: "AI enabled flow article"
---

**AI-enabled length of stay: a lesson in Jidoka**

*Realtime patient flow optimisation guidance for clinicians*

Dr Lucas Zier gave a masterclass in human–machine collaboration last week. His team at Zuckerberg San Francisco General (ZSFG), working with the University of California, San Francisco, has used AI to understand why patients stay in hospital longer than they need to, and then put that understanding to work on the wards every day giving clinicians real time tips on how to optimise patient flow.

Once tuned, the AI pipeline was run across 5000 admissions in five high-volume diagnosis groups. In 30 minutes compute time it independently recovered all six categories from the manual Lean analysis which had looked at 25 patients and had taken 100 person hours:

- **Discharge planning** and post-acute coordination

- **Consult timeliness** and coordination

- **Capacity and coverage**—including weekends

- **Diagnostic turnaround** and procedural workflow

- **Resource use** and capacity management

- **Role clarity** between social work, utilisation management and the acute care team

It then surfaced six themes the manual review had missed, among them late goals-of-care conversations and the management of opioid use disorder on the ward.

The biggest themes are familiar: when social work gets involved, how discharges are coordinated, whether diagnostic work-ups run in parallel or one after another, and what happens at weekends. None of it is exotic. What is new is seeing it counted across hundreds of patients, with every finding traceable back to a line in the record.

The validated pipeline now runs on every admission, every day, using the same notes, orders and timestamps it was validated on. Social work delays, discharge barriers and consult timeliness are computed continuously from the chart.

<img src="/assets/images/uploads/word/ai-enabled-flow-article/media/image1.png" title="Figure 1. From retrospective analysis to continuous support: one validated pipeline feeding two clinical views." style="width:6.25in;height:2.54167in" alt="Figure 1. From retrospective analysis to continuous support: one validated pipeline feeding two clinical views." />

*Figure 1. From retrospective analysis to continuous support: one validated pipeline feeding two clinical views.*

The results are presented in two views. At patient level, clinicians see high-priority discharge tasks in their flow of work: the model reads the chart, suggests tests that may be needed and flags which ones will hold up discharge.

<img src="/assets/images/uploads/word/ai-enabled-flow-article/media/image2.png" title="Figure 2. Patient-level view: a timeline of the stay alongside high-priority discharge tasks. Demonstration screen from the conference presentation." style="width:6.25in;height:3.42708in" alt="Figure 2. Patient-level view: a timeline of the stay alongside high-priority discharge tasks. Demonstration screen from the conference presentation." />

*Figure 2. Patient-level view: a timeline of the stay alongside high-priority discharge tasks. Demonstration screen from the conference presentation.*

At hospital level, care coordinators can see which outstanding tests are blocking discharge across the hospital, ranked by priority, with the model’s reasoning shown alongside each one.

<img src="/assets/images/uploads/word/ai-enabled-flow-article/media/image3.png" title="Figure 3. Hospital-level view: imaging, consult and discharge tasks prioritised by their impact on flow. Demonstration screen from the conference presentation." style="width:6.25in;height:3.32292in" alt="Figure 3. Hospital-level view: imaging, consult and discharge tasks prioritised by their impact on flow. Demonstration screen from the conference presentation." />

*Figure 3. Hospital-level view: imaging, consult and discharge tasks prioritised by their impact on flow. Demonstration screen from the conference presentation.*

This is Jidoka the machine watches every thread continuously and stops to say “this one is about to break”. A person then decides what to do about it.

### **Jidoka, briefly**

Jidoka is the Toyota principle usually translated as automation with a human touch. The classic image is a loom that stops itself the moment a thread breaks, so that a person can come and work out why. The machine does not solve the problem. It makes the abnormality visible and hands it to a human at exactly the right moment.

What makes Jidoka powerful is the division of labour. Machines do what they are good at: tireless detection and repetition. People do what they are good at: judgement, context and improvement. The ZSFG story falls neatly into four steps, and in each one you can see that division at work.

**References**

Schein, E.H. (2013) *Humble Inquiry: The Gentle Art of Asking Instead of Telling*. San Francisco: Berrett-Koehler.

Vossler, P., Feng, J., Sivaraman, V., Gallo, R., Kanzaria, H., Freiser, D., Ross, C., Ou, A., Marks, J., Ehrlich, S., Peabody, C. and Zier, L. (2026a) ‘From fuzzy to formal: scaling hospital quality improvement with AI’, *arXiv* preprint 2604.20055. Available at: <https://arxiv.org/abs/2604.20055>

Vossler, P., Ouyang, J., Guo, F.R., Huang, A., Shojaie, A., Zier, L., Xia, F. and Feng, J. (2026b) ‘Expert-guided g-computation with large language models for estimating causal effects on timings: applications to hospital quality improvement’, *arXiv* preprint 2608.10339. Available at: <https://arxiv.org/abs/2608.10339>
