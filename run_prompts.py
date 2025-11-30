"""Run a predefined list of research prompts sequentially.

This script prints each prompt one-by-one. By default it waits for
confirmation before continuing so you can copy or forward prompts
individually. Use the ``--auto`` flag to stream them without pausing.
"""

from __future__ import annotations

import argparse
from typing import Iterable, List


PROMPTS: List[str] = [
    "Find inference■scaling benchmarks, summarize results, cite sources.",
    "Retrieve KV■cache compression papers and compare reported speedups.",
    "Search 2023–2025 LLM security vulnerabilities with source links.",
    "Summarize enterprise RAG deployment case studies with citations.",
    "Retrieve tokenizer scaling vs quality research with data references.",
    "Find attention■mechanism alternatives and summarize with citations.",
    "Search multilingual LLM evaluation performance (EN–HA–HT).",
    "Document dataset■size vs model■quality research with sources.",
    "Cite primary sources on synthetic■data training improvements.",
    "Explain Mixture■of■Experts routing with academic citations.",
    "Break down transformer attention mathematically with sources.",
    "Describe gradient checkpointing + VRAM impact with benchmarks.",
    "Compare INT8 vs FP16 vs Q4 quantization with citations.",
    "Explain speculative decoding and latency effects with sources.",
    "Summarize positional encoding alternatives with citations.",
    "Define Retrieval■Augmented Generation with real deployments.",
    "Explain distributed multi■GPU training with documentation refs.",
    "Differentiate fine■tuning vs continued pretraining with sources.",
    "Explain token sampling strategies (temp, top■k, top■p) with refs.",
    "Compare Llama■3 vs Qwen■2 benchmarks with citation.",
    "Compare RAG vs Fine■tuning for knowledge integration.",
    "Contrast Perplexity retrieval vs GPT inference quality.",
    "Compare sparse vs dense attention using performance reports.",
    "Analyze long■context scaling across Claude/Gemini/Grok.",
    "Compare 70B vs 405B inference trends using sourced data.",
    "Compare SFT vs RLHF design with academic references.",
    "Contrast FlashAttention v1 vs v2 throughput benchmarks.",
    "Compare GPU vs CPU inference through benchmark studies.",
    "Contrast beam vs nucleus vs contrastive decoding outcomes.",
    "Retrieve scalable RAG pipeline architecture best■practices.",
    "Find open■source LLM evaluation frameworks and compare.",
    "Summarize operational RAG workflows with citations.",
    "Compare vector■DB indexing + scaling strategies with refs.",
    "Retrieve AI■safety eval methodologies used in industry.",
    "Compare model orchestration tools: Ray vs Modal vs HF.",
    "Document distributed inference sharding patterns with refs.",
    "Benchmark embedding models + dataset evaluation results.",
    "Retrieve Perplexity vs GPT integration case studies.",
    "Summarize high■latency inference optimization methods.",
    "Retrieve sci■fi narrative structures, generate new story.",
    "Research AI UX design patterns and generate UI content.",
    "Summarize conversational psychology, derive interaction rules.",
    "Retrieve multilingual brand■tone frameworks, build one.",
    "Research viral behaviour triggers, design marketing plan.",
    "Retrieve futuristic UI visual language and produce style guide.",
    "Summarize persona■generation literature, extract core insights.",
    "Retrieve examples of AI■film scriptwriting, produce new scene.",
    "Find multimodal■AI use■cases and list examples.",
    "Retrieve research on rhythm + emotion, write poem modelled.",
]


def iter_prompts(prompts: Iterable[str], auto: bool) -> None:
    """Print each prompt to stdout, optionally pausing between them."""

    for index, prompt in enumerate(prompts, start=1):
        header = f"Prompt {index}/{len(PROMPTS)}"
        separator = "-" * len(header)
        print(f"\n{header}\n{separator}\n{prompt}\n")
        if not auto and index != len(PROMPTS):
            input("Press Enter to continue to the next prompt...")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Print all prompts without waiting for input between them.",
    )
    args = parser.parse_args()
    iter_prompts(PROMPTS, auto=args.auto)


if __name__ == "__main__":
    main()
