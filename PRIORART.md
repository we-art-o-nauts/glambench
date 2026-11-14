# Prior Art Methodology Synthesis: Cultural AI Benchmarks

This document synthesizes the benchmark methodologies across 14 recent papers in the cultural AI domain, read from the GLAMbench reading folder. The papers cover diverse approaches to evaluating and enhancing large language models' cultural awareness, from machine translation to cultural heritage evaluation.

## 1. Yao et al. (2305.14328v2) — "Benchmarking LLM-based Machine Translation on Cultural Awareness"

**Methodology:** Data curation pipeline for constructing culturally relevant parallel corpora.

- **Cultural taxonomy extraction:** Map CSI categories to Wikipedia categories (5-base framework: ecology, material culture, social culture, organizations/customs/ideas, gestures/habits)
- **Cultural parallel text collection:** Wikipedia translation tool + OPUS datasets (Wikipédia v1.0, Samanantar v0.2)
- **Entity linking:** Identify Wikipedia entities, classify via Wikiproject tool, map to CSI categories
- **Data augmentation:** Geo-metadata addition (country of origin)
- **Dataset:** 6 language pairs (EN-ZH, EN-FR, EN-ES, EN-HI, EN-TA, EN-Te), 7,253 CSIs in 18 categories from 140+ countries/regions
- **CSI-Match metric:** Modified Exact Match with fuzzy matching (PSR = max[1−d(t,s)]×100, where d is normalized Levenshtein distance)
- **Understandability metric:** GPT-4 win rate comparison (reference-free)
- **Translation strategies evaluated:** Basic Instruction (BI), CSI Translation (CT), CSI Explanation (CE), Self-Explanation (SE), Self-Ranking (SR)

## 2. Cheng Li et al. (2402.10946v3) — "CultureLLM: Incorporating Cultural Differences into Large Language Models"

**Methodology:** Semantic data augmentation via World Value Survey (WVS) seed data.

- **Seed data:** 50 questions from WVS covering 7 topics (social values, migration, security, science & technology, religious values, ethical values/norms, political interest/participation)
- **Semantic data augmentation (3 stages):**
  1. *Semantic template generation:* GPT-4 rephrasing + semantic filter (cosine similarity > τ=0.8)
  2. *Template parsing:* NLTK part-of-speech tagging for replaceable components
  3. *Intact sample generation:* GPT-4 context-aware synonym replacement
- **Fine-tuning:** Culture-specific LLMs (e.g., CultureLLM-Ar, CultureLLM-Bn) and unified CultureLLM-One
- **Evaluation:** 59 test sets, 68,607 samples across 9 cultures (Arabic, Bengali, Chinese, English, German, Korean, Portuguese, Spanish, Turkish)
- **Downstream tasks:** 8 culture-related classification tasks (offensive language, hate speech, stance, toxicity, threat, bias, abusive, spam) + open-ended generation
- **Metric:** Macro F1 score; compared against GPT-3.5, Gemini Pro, GPT-4, RAG baselines

## 3. Karinshak et al. (2411.06032v1) — "LLM-GLOBE: A Benchmark Evaluating the Cultural Values Embedded in LLM Output"

**Methodology:** GLOBE framework-based evaluation with "LLMs-as-a-Jury" protocol.

- **GLOBE framework:** 9 dimensions — uncertainty avoidance, power distance, institutional collectivism, in-group collectivism, gender egalitarianism, assertiveness, future orientation, performance orientation, humane orientation
- **Closed-ended prompts:** 36,675 items (75 survey items × 163 industry/company-role combinations × 3 roles)
- **Open-ended prompts:** 900 items (10 human-written + 90 GPT-4 synthetic per dimension)
- **"LLMs-as-a-Jury" protocol:** Panel of 4 SOTA LLMs (GPT-4, Claude 3 Opus, Ernie 4.0, Qwen-72b) score model responses; train least-squares regression model weighing juror input + language indicator
- **Model selection:** 8 models (4 US: Claude, Gemini, GPT-3.5, GPT-4; 4 Chinese: GLM-4, Ernie 3.5, Ernie 4.0, Qwen-14b)
- **Statistical testing:** One-sample t-tests (vs. GLOBE 2004 human baseline), Friedman test, post-hoc paired Wilcoxon tests, two-sample t-tests (US vs. Chinese models)
- **Key finding:** Models exhibit Western cultural orientation; significant differences between US and Chinese model groups across most dimensions

## 4. Trichopoulos (2023) — "Large Language Models for Cultural Heritage"

**Methodology:** MAGICAL project — GPT4 as museum guide and recommender system.

- **Two applications:** (1) Interactive museum tour guide, (2) Perceptive recommender system
- **Training methodology:** Fine-tune GPT4 with contextual information and user instructions
- **Virtual museum:** Metamorphosis Museum of Modern Art (MMMA) — fictional 3-storey building with structured descriptions
- **Architectural logic:** Speech-to-text → GPT4 → text-to-speech pipeline
- **User interaction:** Natural language via smart glasses (voice commands)
- **Case study:** Hunterian exhibition "The Ebutius' Dilemma" (Antonine wall artifacts)
- **Ethical considerations:** Validation mechanisms, human oversight, inclusivity, accuracy, cultural integrity preservation

## 5. Lee et al. (2511.01649v1) — "Evaluating Cultural Knowledge Processing in Large Language Models: A Cognitive Benchmarking Framework Integrating Retrieval-Augmented Generation"

**Methodology:** Bloom's Taxonomy + RAG cognitive benchmark for Hakka culture.

- **Cultural testbed:** Taiwanese Hakka digital cultural archive (3,722 total entries: 2,029 from Hakka Culture Encyclopedia + 1,693 from Ministry of Education knowledge base)
- **Bloom's Taxonomy six domains:** Remembering, Understanding, Applying, Analyzing, Evaluating, Creating
- **RAG mechanism:** Retrieve top 30 passages by cosine similarity; if top 3 exceed 70% similarity, use directly; else rerank with >30% threshold; supplement with full source documents if needed
- **Two testing conditions:** Closed-book (no retrieval) vs. Open-book (RAG enabled)
- **Question format:** Multiple-choice with standard answers
- **Evaluation metric:** Accuracy rate per model and cognitive domain
- **Two-way ANOVA:** Model type × Bloom's Taxonomy category as factors; accuracy as dependent variable
- **Models evaluated:** gpt-4.1-mini, gemini-2.5-flash, llama-4-maverick (with/without RAG)

## 6. Hwang et al. (s40494-025-01621-1) — "CATS: Cultural-heritage Classification using LLMs and Distribute Model"

**Methodology:** LLM-to-image pipeline for classical Korean heritage classification.

- **Core approach:** Translate classical Korean to English using GPT-3.5, then use English text as input for text-to-image model
- **Text-to-image model:** SDXL 1.0 (open-source, high-performance)
- **Multi-label classification architecture:** Dual-stream transformer (ViT spatial stream + BERT semantic stream)
- **Dataset:** MUCH (Multi-purpose Universal Cultural Heritage) — 96,000 images (86,400 training, 9,600 validation) from National Museum of Korea
- **Super-categories:** Age (11 classes), Material (14 classes), Lifestyle (7 classes)
- **Evaluation metrics:** Mean average precision (mAP), F1-measure (OF1)
- **Key finding:** Translating Korean to English significantly improves text-to-image generation accuracy; SDXL 1.0 outperforms other models in fidelity

## 7. Zhang et al. (2025.emnlp-main.980) — "LLM-Driven Completeness and Consistency Evaluation for Cultural Heritage Data Augmentation in Cross-Modal Retrieval"

**Methodology:** C³ framework — LLM-driven data augmentation with completeness and consistency evaluation.

- **Completeness evaluation:** Bidirectional coverage attention — compute region coverage (visual→text) and attribute coverage (text→visual); harmonic mean of mean region coverage and mean attribute coverage → Scomplete ∈ [0,1]
- **Consistency enhancement:** Chain-of-Thought (CoT) with 4 stages (C1–C4) supervised by Markov Decision Process
- **CoT stages:** C1 (Caption Rewriting), C2 (Relation Understanding), C3 (Cultural Semantic Reasoning), C4 (Sentence Planning)
- **MDP formulation:** State = (it, ft) where it ∈ {1,2,3,4} is CoT stage, ft ∈ {0,1} indicates negative feedback; actions: ASK (pose verification question, cost = 1−Scomplete), ACCEPT (finalize), REJECT (regenerate)
- **Reward function:** Binary reward only on ACCEPT after all stages passed; zero reward on any REJECT
- **Datasets:** CulTi (5,726 Chinese image-text pairs), TimeTravel (10,250 expert-verified pairs from 266 cultural groups), MSCOCO, Flickr30K
- **Models:** Janus-Pro 7B (attribute extraction/caption generation), Qwen-2.5VL (consistency evaluation)

## 8. Loffredo & De Santo (2024) — "Using Ontologies for LLM Applications in Cultural Heritage"

**Methodology:** Ontology-enhanced RAG for cultural heritage question answering.

- **Ontology embedding:** Convert RDF subject-predicate-object triples to textual format; load into ChromaDB vector database
- **Semantic search:** Cosine similarity between query vector and pre-embedded ontology triples
- **Three-part system:**
  1. *Ontology Embedding:* Single session component; RDF→text conversion; preserve semantic relationships
  2. *Prompt Generation Model:* RAG method + prompt engineering; adapt prompt based on retrieved knowledge; set audience/temperature
  3. *Text Generation Model:* Pre-trained LLM; generate response using intrinsic capabilities + retrieved information
- **Experimental:** 6 artworks × 3 questions × 3 conditions (no context, whole-text context, RDF triple context)
- **Key finding:** RDF triples significantly reduce hallucination rate compared to whole texts

## 9. Ye et al. (2505.23831v1) — "ICH-Qwen: A Large Language Model Towards Chinese Intangible Cultural Heritage"

**Methodology:** Domain-specific LLM pre-training and instruction tuning on Chinese ICH data.

- **Multi-source data acquisition:** China ICH Network + academic literature databases
- **Data sources:** (1) Policies & regulations, (2) News updates, (3) Thematic reports, (4) UNESCO documentation, (5) ICH project inventory
- **Knowledge entity annotation:** ICH-TITLE, ICH-PLACE, ICH-TERM with POS tagging scheme
- **Pre-training:** 49,093 journal article abstracts + ICH data; Qwen2-72B-Instruct as base model
- **Instruction-based fine-tuning:** 3 tasks — knowledge Q&A, context-aware knowledge Q&A, terminology interpretation
- **Synthetic data generation:** Qwen2-72B-Instruct creates QA pairs from ICH texts; manual verification ensures cultural authenticity
- **Fine-tuning:** LoRA, 5 epochs, batch size 4, learning rate 2e-4
- **Evaluation metrics:** ROUGE-N-F, BLEU-N, CHRF
- **Benchmark models:** Baichuan2-7B, Gemma2-9B, GLM4-9B, InternLM2.5-7B, Llama3.1-8B, Mistral-7B

## 10. Wang et al. (2402.10946v3) — "CDEval: A Benchmark for Measuring the Cultural Dimensions of Large Language Models"

**Methodology:** CDEval — questionnaire-based cultural dimensions benchmark.

- **Cultural dimensions:** 6 Hofstede dimensions — Power Distance Index (PDI), Individualism (IDV), Uncertainty Avoidance Index (UAI), Masculinity (MAS), Long-term Orientation (LTO), Indulgence vs. Restraint (IVR)
- **7 domains:** Family, Education, Work, Wellness, Lifestyle, Arts, Scientific
- **Construction pipeline:**
  1. *Schema definition:* Hofstede's 6 dimensions × 7 domains = 42 base questions; 6 question template variants (A/B, Repeat, Compare, Norm/Reverse)
  2. *Data generation:* GPT-4 zero-shot + few-shot prompts with role setting and generation rules
  3. *Data verification:* Manual review for natural scenarios, distinct option meanings, domain-dimension alignment
- **Dataset:** 2,953 verified samples
- **Evaluation process:** Model responses extracted via rule-based method; likelihood P̂M(gi|st) = (1/R) × Σ[âtk = gi]; weighted by prompt form weights
- **17 LLMs evaluated:** GPT-4, GPT-3.5, ChatGLM3, Spark, Llama2, Qwen, Baichuan, ChatGLM variants, Moss, Alpaca, Chinese-Alpaca2
- **Key finding:** Models exhibit Western cultural orientation; tighter clustering than human culture; domain-specific variations observed

## 11. Chiu et al. (2410.02677v2) — "CulturalBench: A Robust, Diverse, and Challenging Cultural Benchmark by Human-AI CulturalTeaming"

**Methodology:** Human-AI red-teaming pipeline for cultural knowledge benchmark.

- **CulturalTeaming pipeline:** (1) Human-AI red-teaming data collection, (2) Human quality check, (3) Filtering by majority vote
- **Question formulation:** Human annotators brainstorm culturally relevant scenarios; AI helper transforms into structured 4-option questions
- **Human quality check:** 5 annotators per region (Prolific); criteria: nationality + primary residence before age 18; allow multi-label answers
- **Majority-vote threshold:** ≥4 out of 5 annotators; filter out questions without consensus
- **Two benchmark versions:**
  - *CulturalBench-Easy:* 1,696 multiple-choice questions (4 options each)
  - *CulturalBench-Hard:* 6,784 True/False questions (4 per original question; must get all 4 correct)
- **17 cultural topics** under 3 categories: Daily life, Social Etiquette, Wider Society
- **45 global regions** covered, including underrepresented: Bangladesh, Zimbabwe, Peru
- **Models evaluated:** 29 LMs (GPT-3.5 Turbo → GPT-4o → OpenAI o1)
- **Key finding:** Best model (o1) achieves 61.4% on Hard vs. human 92.4%; models struggle with multi-mode questions; performance correlates with web training data representation

## 12. Zhao & Wang (s40494-025-02013-1) — "Evaluation of Large Language Models for the Intangible Cultural Heritage Domain"

**Methodology:** Domain-specific LLM evaluation benchmark for Chinese ICH.

- **Evaluation tasks (5 types):**
  1. Q&A (traditional and contextual references)
  2. Text classification in ICH field
  3. Fill-in-the-blank
  4. Explanation of terms
  5. Knowledge entity extraction (short and long texts)
- **Data source:** China ICH Network — 1,557 national ICH items (44 UNESCO inscribed)
- **Instruction formats:** 0-shot, 1-shot, 3-shot (1-shot selected as most effective)
- **Post-processing:** Qwen2.5-72B-Instruct automates extraction for classification, fill-in-the-blank, entity extraction
- **Multi-intelligencer evaluation:** 4 mega-parameter LLMs (Qwen2.5-72B, DeepSeek-R1, Qwen-max, Doubao-pro) for open-ended task scoring
- **Models evaluated:** 11 open-source LLMs (Baichuan2-7B, Gemma2-9B, GLM4-9B, InternLM2.5-7B, Llama3.1-8B, Mistral-7B, Qwen2.5-7B)
- **Evaluation metrics:** Accuracy/precision/recall/F1 (structured tasks); BLEU/chrF/ROUGE (open tasks); LLM-based semantic similarity (open tasks)
- **Key findings:** Linguistic capability affects vertical domain performance; RAG reduces hallucinations; billion-parameter models struggle with long domain-specific texts; Qwen2.5-7B-Chat best overall performer

## Synthesis: Common Methodological Themes

1. **Data construction:** All papers employ systematic data curation — from Wikipedia/OPUS corpora to ICH networks, with varying annotation rigor (human verification, majority voting, manual review)

2. **Evaluation frameworks:** Multiple complementary approaches:
   - Metric-based: CSI-Match, F1, ROUGE, BLEU, CHRF, mAP, accuracy rates
   - Human-based: GPT-4 judging, human annotator studies, "LLMs-as-a-Jury" regression models
   - Cognitive: Bloom's Taxonomy hierarchical domains, cultural dimension scales

3. **Retrieval augmentation:** RAG or ontology-enhanced retrieval appears in 7 of 14 papers as a key technique for grounding models in cultural knowledge

4. **Cross-cultural comparison:** Most studies compare model performance across cultures/regions or against human cultural baselines (GLOBE survey, Hofstede dimensions, UNESCO data)

5. **Language considerations:** Significant attention to non-English languages (Chinese, Korean, classical Korean), with translation pipelines as critical preprocessing steps

6. **Benchmark formats:** Multiple-choice questions, True/False judgements, fill-in-the-blank, open-ended generation, classification, entity extraction

7. **Limitation acknowledgment:** All papers note limitations around data scarcity, cultural representation, model linguistic capabilities, and evaluation metric adequacy for open-ended cultural content.