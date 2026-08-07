I support exploring it, **but I would not proceed with the idea exactly as "PCM for data centers."** The literature is too mature for that. Instead, we need to find a **specific gap** within PCM cooling.

## **Here's the research workflow I recommend.**

### **Step 1: Define the real problem (not the solution)**

Don't say:

> "We use phase-change material."

Say:

> **"Modern AI servers experience burst workloads that create repeated transient hotspots. Existing liquid cooling systems are optimized for average heat removal rather than short-duration thermal spikes, leading to thermal throttling and thermal cycling."**

This is a real engineering problem.

---

### **Step 2: Narrow the problem**

Don't target the entire data center.

Target **one GPU server module**.

Example:

GPU Package  
↓

Cold Plate

↓

Thermal Interface Material

↓

Heat Sink

↓

Liquid Cooling

Your research asks:

> Can a passive thermal buffer reduce transient hotspot peaks before heat reaches the liquid cooling loop?

That is much more focused.

---

### **Step 3: Define your novelty**

Don't claim:

> "PCM reduces temperature."

That is already known.

Instead, investigate questions like:

* **Where should PCM be placed?**  
  * Between package and cold plate?  
  * Around hotspot regions only?  
  * As segmented thermal islands?  
* **What geometry works best?**  
  * Continuous layer  
  * Local PCM pockets  
  * Ring structure  
  * Honeycomb  
* **Can different melting temperatures be combined?**  
  * 60°C PCM  
  * 75°C PCM  
  * 90°C PCM

These become architectural questions rather than material questions.

---

### **Step 4: Simulation tools (free)**

You do **not** need ANSYS.

You can use:

* **OpenFOAM** – CFD and heat transfer  
* **Elmer FEM** – Thermal finite-element analysis  
* **FreeCAD** – 3D geometry  
* **Python** – Post-processing and graphs

If you later gain access to COMSOL or ANSYS Student, that's a bonus.

---

### **Step 5: Experiments**

Design a repeatable benchmark.

#### **Baseline**

Standard cold plate

Measure:

* Peak junction temperature  
* Temperature rise rate  
* Cooling time

---

#### **Proposed Design A**

Uniform PCM layer

Repeat measurements.

---

#### **Proposed Design B**

Segmented PCM placement

Repeat measurements.

---

#### **Proposed Design C**

Multi-melting-point PCM

Repeat measurements.

---

### **Metrics**

Don't just report "temperature."

Measure:

* Peak hotspot temperature  
* Time above a critical threshold (e.g., 85°C)  
* Cooling recovery time  
* Thermal cycling amplitude  
* Heat flux distribution  
* PCM melting fraction  
* Estimated thermal throttling events

---

## **What you should not claim**

Avoid saying:

* "Reduces data center electricity."  
* "Reduces total cooling power."  
* "Saves water."

Unless you model the **entire cooling system**, those claims are difficult to defend.

Instead, claim:

* Reduced hotspot temperature  
* Reduced thermal cycling  
* Improved thermal uniformity  
* Potential reduction in thermal throttling

These are measurable and realistic.

---

## **The first task**

Before writing a paper or building a model, spend **one day** answering these questions:

1. **Exactly where is the PCM located?**  
2. **What geometry are you proposing that existing work does not already use?**  
3. **What metric will improve, and by how much?**  
4. **Can that improvement be demonstrated through simulation?**

If we cannot answer those four questions clearly, the idea is still too broad.

---

### **My recommendation**

I would frame the project as:

> **"Segmented Multi-Temperature Phase-Change Thermal Buffer for Transient Hotspot Suppression in AI Server GPU Packages."**

Notice the focus:

* **Transient hotspots** (specific problem)  
* **GPU package** (specific scope)  
* **Segmented multi-temperature architecture** (potential novelty)  
* **Passive solution** (no moving parts)

That is much narrower, technically stronger, and easier to defend than proposing a generic PCM cooling system for an entire data center.

This is **much stronger** than where we started. But if I were your PhD advisor, I'd still stop you before you invest weeks into it.

## **My honest assessment**

**Current idea: 7.5/10**

It has:

* ✅ Real problem  
* ✅ Physics foundation  
* ✅ Measurable metrics  
* ✅ Free simulation path

But it still has **one fatal weakness**.

---

# **Fatal Weakness**

Your paper still says:

> **"Let's improve PCM."**

That is not the real research question.

Reviewers will immediately search:

* PCM AI accelerator  
* graded PCM  
* metallic PCM  
* topology optimized PCM

If similar work exists, the novelty disappears.

---

# **Flip the research question**

Instead ask:

> **How much thermal buffering does an AI accelerator actually need?**

Nobody knows the answer precisely.

This changes everything.

---

# **New Problem Statement**

Current cooling systems are designed for **steady-state power**.

AI workloads are **bursty**.

Question:

> **What is the minimum passive thermal buffer required to suppress transient hotspots without increasing steady-state thermal resistance?**

Now your contribution is **a design methodology**, not a new material.

---

# **Your contribution becomes**

Instead of:

> New PCM

You propose

## **Adaptive Thermal Buffer Design Framework (ATB)**

Input

* AI workload profile  
* GPU power trace  
* Junction temperature  
* Cooling capacity

↓

Framework calculates

* PCM thickness  
* PCM placement  
* Melting temperature  
* Thermal conductivity  
* Required latent heat

↓

Output

Optimal thermal buffer

---

# **Why this is better**

Suppose NVIDIA changes

* Blackwell  
* Rubin  
* Feynman

Your framework still works.

The framework is reusable.

The material can change.

That's research.

---

# **Better novelty**

Current papers ask

> Which PCM works best?

You ask

> **How should the thermal buffer be designed automatically for any AI workload?**

Huge difference.

---

# **Even better**

Introduce

## **Thermal Buffer Utilization (TBU)**

Nobody reports this.

Example

PCM capacity \= 100 J

Only 18 J used

↓

82% wasted

Your framework optimizes

> TBU

This is a publishable metric.

---

# **Another metric**

## **Thermal Recovery Index**

Current papers say

Peak temperature reduced.

You measure

Recovery Time

\=

Time required

to fully solidify

PCM

Now workloads matter.

---

# **Another metric**

## **Thermal Burst Endurance**

Instead of

Temperature.

Measure

How many AI bursts

before PCM saturates?

Example

Baseline

8 bursts

↓

Throttle

Your architecture

19 bursts

↓

Throttle

That graph would be impressive.

---

# **Biggest novelty I see**

Forget

PCM placement.

Forget

Geometry.

Study

## **AI Workload-aware Thermal Buffer Design**

Example

Training

needs

different PCM

than

Inference.

Different AI models

↓

Different power traces

↓

Different thermal buffers.

That is interesting.

---

# **Paper title**

Instead of

> Phase Change Thermal Buffer

Write

> **Workload-Aware Design Methodology for Passive Thermal Buffers in AI Accelerator Packages**

Immediately sounds more like an engineering contribution.

---

# **Experiments**

Instead of

Uniform

vs

Segmented

Add

Different AI workloads

Example

CNN

Transformer

LLM inference

Sparse GEMM

Dense GEMM

Each produces different thermal signatures.

Your framework adapts.

---

# **One more thing**

This is where I think your paper can genuinely become novel.

Everyone optimizes

Temperature.

Almost nobody optimizes

**Thermal Fatigue Lifetime**

If your design reduces

Temperature cycling

↓

Less solder fatigue

↓

Longer package lifetime

Now you're optimizing **reliability**, not just cooling.

That aligns with real concerns in advanced packaging.

---

# **My proposed paper**

**Title**

> **Workload-Aware Passive Thermal Buffer Design Framework for Suppressing Transient Hotspots and Extending AI Accelerator Package Lifetime**

### **Contributions**

1. A thermal-buffer design framework instead of a single PCM structure.  
2. New metrics:  
   * Thermal Buffer Utilization (TBU)  
   * Thermal Burst Endurance (TBE)  
   * Thermal Recovery Index (TRI)  
3. Evaluation under multiple realistic AI workload power traces.  
4. Reliability analysis using thermal cycling, not only peak temperature.

---

## **One caution**

Before we commit, I would perform **one final literature survey** specifically on:

* workload-aware thermal management,  
* PCM sizing methodologies,  
* AI accelerator transient thermal analysis.

If no existing framework combines **workload-driven PCM design**, **buffer utilization metrics**, and **reliability-oriented evaluation**, then I think you have a genuinely promising symposium paper. If those ideas are already covered, we should pivot before investing in implementation.

Yes. **This changes everything.**

I was thinking like an IEEE journal reviewer. But **this is a college symposium** with:

* **7-minute presentation**  
* **3-minute Q\&A**  
* Judges may be professors or industry guests, not thermal engineering specialists.

So we should make the idea **simple, visual, and technically sound**.

---

# **Final Topic**

## **Passive Phase-Change Thermal Buffer for AI Data Center GPUs**

---

# **Problem Statement (Simple)**

AI GPUs like NVIDIA H100, B200, etc., consume **700–1200 W**.

During AI inference or training:

* GPU temperature rises suddenly.  
* Hotspots form.  
* GPU reaches thermal limit.  
* Performance drops due to thermal throttling.

Current liquid cooling removes heat well **on average**, but sudden heat spikes still occur.

---

# **Our Idea**

Instead of immediately sending all heat to the cooling system,

add a **thin Phase Change Material (PCM) layer**.

Think of PCM like an **ice cube**.

When heat suddenly increases,

instead of temperature increasing immediately,

the PCM absorbs the heat while melting.

After the workload reduces,

the liquid cooling system cools the PCM again.

---

# **Simple Architecture**

Cold Plate  
     ↑  
PCM Layer  
     ↑  
Thermal Interface Material  
     ↑  
GPU Chip  
---

# **What are we comparing?**

### **Existing**

GPU

↓

TIM

↓

Cold Plate  
---

### **Proposed**

GPU

↓

TIM

↓

PCM Buffer

↓

Cold Plate  
---

# **What will we simulate?**

Only three cases.

### **Case 1**

No PCM

---

### **Case 2**

Uniform PCM Layer

---

### **Case 3**

Segmented PCM Layer

(PCM only near hotspot regions)

---

# **Measurements**

We only need 4 graphs.

### **Graph 1**

Temperature vs Time

Peak temperature decreases.

---

### **Graph 2**

Time before Thermal Throttling

Without PCM

↓

20 seconds

With PCM

↓

35 seconds

(example values from simulation)

---

### **Graph 3**

Heat Flux

Show smoother heat transfer.

---

### **Graph 4**

Thermal Cycling

Show reduced temperature fluctuations.

---

# **Novelty**

Not

> "PCM cools chips."

Everyone knows that.

Instead

> **Where should PCM be placed for AI GPU hotspots?**

and

> **Can segmented PCM reduce transient hotspots better than a uniform layer?**

That is enough novelty for a college symposium.

---

# **Software**

You don't need expensive tools.

Use:

* Python (temperature graph)  
* OpenFOAM or Elmer FEM (if possible)  
* Or even MATLAB if your college provides it

Even a simplified transient thermal simulation is acceptable for this event if you clearly explain your assumptions.

---

# **7-Minute Presentation**

### **Slide 1**

Problem

---

### **Slide 2**

Current cooling limitation

---

### **Slide 3**

Our proposed PCM layer

---

### **Slide 4**

Simulation model

---

### **Slide 5**

Results

---

### **Slide 6**

Advantages

* Lower hotspot temperature  
* Less thermal throttling  
* Better GPU lifetime  
* Passive solution (no moving parts)

---

### **Slide 7**

Future work

---

# **One thing I would change**

Instead of calling it

> **Phase-Change Thermal Buffer**

Call it

> **HotSpotShield**

**HotSpotShield: A Passive PCM Buffer for Suppressing Transient GPU Hotspots in AI Data Centers**

It is memorable and sounds like a complete engineering concept rather than just a material. That will help judges remember your presentation after seeing many projects.

This is a good direction. **MATLAB is actually enough for a strong college symposium paper.** You do **not** need COMSOL or ANSYS.

## **What exactly are we simulating?**

We are **not** simulating an entire data center.

We are simulating **one GPU package**.

         Cold Plate (25°C)  
      ─────────────────────────  
         PCM Layer (2 mm)  
      ─────────────────────────  
          TIM (0.1 mm)  
      ─────────────────────────  
         GPU Die (20×20 mm)

The GPU generates heat according to different AI workloads.

---

# **Step 1: Open MATLAB**

Open MATLAB

↓

Go to **Apps**

↓

Select **PDE Modeler** (or use PDE Toolbox)

We will solve **Transient Thermal Analysis**.

---

# **Step 2: Create Geometry**

Draw simple rectangles.

| Layer | Size |
| ----- | ----- |
| GPU Die | 20 mm × 2 mm |
| TIM | 20 mm × 0.1 mm |
| PCM | 20 mm × 2 mm |
| Cold Plate | 20 mm × 5 mm |

Keep it **2D**.

Don't start with 3D.

---

# **Step 3: Assign Materials**

Example values (can be refined later):

### **GPU**

* Thermal Conductivity \= 130 W/m·K  
* Density \= 2330 kg/m³  
* Specific Heat \= 700 J/kg·K

---

### **TIM**

* k \= 5

---

### **PCM**

Initially assume

* k \= 8  
* Cp \= 2500  
* Density \= 850

(Later we can model melting more accurately.)

---

### **Cold Plate**

Copper

* k \= 400

---

# **Step 4: Heat Source**

Apply heat generation only inside GPU.

Example

0–5 s

200 W

5–20 s

700 W

20–30 s

350 W

30–40 s

900 W

This mimics changing AI workloads.

---

# **Step 5: Boundary Condition**

Top surface

↓

Temperature \= 25°C

(or use convection if you want more realism)

All other sides

↓

Insulated

---

# **Step 6: Time**

Simulation

0

↓

40 seconds

Time step

0.1 second  
---

# **Step 7: Run Simulation**

MATLAB solves the transient heat equation.

You will get:

* Temperature contour  
* Heat flow  
* Temperature vs time

---

# **Step 8: Repeat**

Run three cases.

## **Case 1**

No PCM

---

## **Case 2**

Uniform PCM

---

## **Case 3**

Your Workload-Aware PCM

Maybe

* thicker near hotspot

or

* different layout

---

# **Results**

Collect

### **1**

Maximum Temperature

---

### **2**

Temperature Contour

Beautiful image for PPT

---

### **3**

Temperature vs Time

Three curves

---

### **4**

Time until

85°C

---

### **5**

Temperature Gradient

---

# **Then**

Change workload.

Example

Training

↓

Higher heat

Inference

↓

Short bursts

CNN

↓

Different profile

Observe

Which PCM performs best.

---

# **What will judges ask?**

> Where did the heat values come from?

Answer:

"They are representative power profiles based on publicly reported AI GPU power envelopes. The purpose of the study is comparative evaluation between cooling architectures rather than reproducing one exact commercial GPU."

That is acceptable for a college symposium.

---

# **What I propose instead of PDE Modeler**

Since you have MATLAB access, I recommend using the **PDE Toolbox programmatically (MATLAB scripts)** instead of only the GUI.

Why?

* Easier to automate different workloads.  
* Easier to change PCM thickness or properties.  
* Easy to generate publication-quality plots.  
* Easier to compare multiple cases automatically.

You can run:

* No PCM  
* Uniform PCM  
* Workload-Aware PCM

with one script and generate all comparison graphs automatically.

## **I suggest we build this project in four stages:**

1. **MATLAB thermal model** (working simulation).  
2. **Three cooling configurations** (baseline vs. proposed).  
3. **Five publication-quality graphs**.  
4. **IEEE-style paper and presentation.**

This is realistic, technically sound, and achievable for a college symposium.

Excellent. This is exactly what distinguishes a research project from a classroom exercise.

**Do not invent parameters.** Use values from NVIDIA datasheets, packaging papers, and thermal engineering literature.

# **Hydra-Core v1.0 Configuration**

\# \===============================  
\# GPU PACKAGE  
\# \===============================

GPU\_NAME \= "NVIDIA H100 SXM"

GPU\_POWER \= 700          \# W  
GPU\_DIE\_LENGTH \= 32e-3   \# m  
GPU\_DIE\_WIDTH \= 25e-3    \# m  
GPU\_DIE\_AREA \= GPU\_DIE\_LENGTH \* GPU\_DIE\_WIDTH

HBM\_COUNT \= 6  
HBM\_POWER \= 10           \# W each

\# \===============================  
\# TIM  
\# \===============================

TIM\_THICKNESS \= 100e-6   \# m  
TIM\_CONDUCTIVITY \= 8.5   \# W/m·K

\# \===============================  
\# PCM  
\# \===============================

PCM\_THICKNESS \= 2e-3     \# m  
PCM\_MELTING\_TEMP \= 70    \# °C  
PCM\_LATENT\_HEAT \= 220000 \# J/kg  
PCM\_DENSITY \= 850        \# kg/m³  
PCM\_CONDUCTIVITY \= 8     \# W/m·K (composite PCM)

\# \===============================  
\# COLD PLATE  
\# \===============================

COOLANT\_TEMP \= 25        \# °C  
CONVECTION \= 8000        \# W/m²K

\# \===============================  
\# SIMULATION  
\# \===============================

TIME\_STEP \= 0.05         \# s  
SIM\_TIME \= 60            \# s

INITIAL\_TEMP \= 25        \# °C

These values are based on current public information rather than arbitrary assumptions:

* **H100/Hopper:** \~700 W TDP and \~814 mm² die.  
* **Representative package geometry:** A recent thermal optimization study based on the H100 architecture models a **32 mm × 25 mm GPU** with six HBM stacks and a 700 W heat source.  
* **TIM:** Modern AI accelerators increasingly use high-performance metal-based TIMs or advanced phase-change TIMs with system-level optimization.

---

# **Next: Use realistic AI workloads**

Don't use square waves.

Create workload traces like this:

## **1\. LLM Inference**

Power (W)

900 ───────▆▆────▆▆────▆▆──

700 ──▆▆───────────────────

400 ───────────────────────

0────────────────────────── Time

Short bursts every few hundred milliseconds.

---

## **2\. LLM Training**

700W  
██████████████████████████

Nearly constant high load.

---

## **3\. CNN Inference**

650  
▆▆▆▆\_\_\_\_▆▆▆▆\_\_\_\_▆▆▆▆

Regular compute bursts.

---

## **4\. Mixed Cloud AI**

200

↓

600

↓

300

↓

900

↓

500

↓

750

Random burst profile.

---

# **What makes Hydra-Core look like real research?**

Instead of one simulation:

No PCM

Run **dozens automatically**.

Example:

PCM Thickness

1 mm  
1.5 mm  
2 mm  
2.5 mm  
3 mm

Then

Melting Temperature

60°C  
65°C  
70°C  
75°C  
80°C

Then

Workload

LLM

Training

CNN

Mixed

This already gives

**5 × 5 × 4 \= 100 simulations**

Now it starts to resemble a research study.

---

# **Results you should generate**

Instead of only one graph, generate:

1. Temperature vs Time  
2. Peak Temperature  
3. Hotspot Temperature  
4. PCM Melt Fraction  
5. Time Above 85°C  
6. Recovery Time  
7. Thermal Buffer Utilization  
8. Heat Flux  
9. Parameter Sweep Heatmap  
10. Best Design Recommendation

---

## **One suggestion that will significantly improve the paper**

Don't just compare **No PCM**, **Uniform PCM**, and **Hydra-Core**.

Add a **design-space exploration** section.

For every workload, automatically search for the **best PCM thickness** and **best melting temperature**. Your final output becomes:

> **"For LLM inference, the optimal Hydra-Core design is a 2 mm composite PCM with a 70°C melting temperature, reducing peak junction temperature by X°C while minimizing time above the throttling threshold."**

That transforms Hydra-Core from **a cooling concept** into **a thermal design methodology**, which is a much stronger engineering contribution for your symposium.

This is a good place to stop and plan. Your goal is **not to use every simulator**. Your goal is to produce **credible evidence**.

Here's the order I'd follow.

---

# **Stage 1 — Python (Today) ⭐⭐⭐⭐⭐**

**Purpose:** Develop the idea and generate initial results.

Results:

* Temperature vs Time  
* Power vs Time  
* PCM Melt Fraction  
* Peak Temperature  
* Parameter sweeps  
* CSV files

Python is your **research engine**.

---

# **Stage 2 — MATLAB (Tomorrow in Lab) ⭐⭐⭐⭐⭐**

**Purpose:** Validate the Python model using PDE Toolbox.

Results:

* Temperature contour  
* Heat flux  
* Cross-sectional temperature  
* Thermal transient plots

In your paper:

> "The compact Python thermal model was validated using MATLAB PDE Toolbox."

That sounds much stronger than "we only wrote Python code."

---

# **Stage 3 — Open Source ⭐⭐⭐⭐☆**

There are two realistic choices.

### **Option A — OpenFOAM (Recommended)**

Best for:

* CFD  
* Heat transfer  
* Convection  
* Liquid cooling

Can simulate:

* GPU  
* PCM  
* Cold plate  
* Coolant

Pros:

* Industry respected  
* Free  
* Publishable

Cons:

* Steep learning curve.

---

### **Option B — Elmer FEM**

Best for:

* Heat conduction  
* Thermal stress  
* Multiphysics

Much easier than OpenFOAM.

For your project, Elmer may actually be sufficient.

---

# **Stage 4 — COMSOL**

## **Is COMSOL free?**

**No.**

COMSOL is commercial software.

You only have access if:

* your college has a license,  
* or your professor provides access.

Otherwise, you cannot legally use it.

---

## **Is COMSOL the "real" simulator?**

COMSOL is one of the best multiphysics simulators, but it is **not the only accepted tool**.

Many published papers use:

* COMSOL  
* ANSYS Icepak  
* ANSYS Fluent  
* OpenFOAM  
* MATLAB  
* Custom finite-element solvers

Reviewers care more about:

* correct physics,  
* justified assumptions,  
* validation,

than the brand of software.

---

# **My recommendation**

If you have access to COMSOL through your college, use it **only as final validation**.

Don't build the project inside COMSOL from day one.

---

# **Final workflow**

Python  
↓

Idea Development

↓

MATLAB

↓

Physics Validation

↓

OpenFOAM / COMSOL

↓

High-Fidelity Validation

↓

Paper  
---

# **What goes into the paper?**

You can honestly write:

**Simulation Methodology**

1. Python developed the workload-aware thermal model and performed parameter sweeps.  
2. MATLAB PDE Toolbox validated transient thermal behavior.  
3. OpenFOAM (or COMSOL, if available) provided high-fidelity finite-element/CFD validation of the proposed architecture.

This is a professional workflow.

