import { createFileRoute } from "@tanstack/react-router";
import { useState, useRef } from "react";
import ReactMarkdown from "react-markdown";
import { ArrowUp, Loader2, Sparkles } from "lucide-react";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Brochure Generator — AI-powered company brochures" },
      {
        name: "description",
        content:
          "Generate a beautiful company brochure from any website URL using AI. Pick a model, paste a URL, and ship.",
      },
      { property: "og:title", content: "Brochure Generator" },
      {
        property: "og:description",
        content: "Generate a beautiful company brochure from any website URL using AI.",
      },
    ],
  }),
  component: Index,
});

const MODELS = [
  { value: "CHATGPT", label: "ChatGPT (gpt-oss-20b)" },
  { value: "GEMMA", label: "Gemma" },
  { value: "META", label: "Llama 3.2" },
  { value: "LIQUID", label: "Liquid LFM" },
  { value: "QWEN", label: "Qwen 3 Coder" },
  { value: "HERMES", label: "Hermes 3" },
  { value: "NEX", label: "Nex N2 Pro" },
  { value: "VENICE", label: "Dolphin Venice" },
];

const EXAMPLES = [
  { name: "Hugging Face", url: "https://huggingface.co" },
  { name: "DeepMind", url: "https://deepmind.com" },
  { name: "OpenAI", url: "https://openai.com" },
];

const API_URL =
  (import.meta.env.VITE_BROCHURE_API_URL as string | undefined) ??
  "http://localhost:8000/generate-brochure";

function Index() {
  const [company, setCompany] = useState("");
  const [url, setUrl] = useState("");
  const [model, setModel] = useState("CHATGPT");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const abortRef = useRef<AbortController | null>(null);
  const contentRef = useRef<HTMLDivElement>(null);
  const [copied, setCopied] = useState(false);

  const canSubmit = company.trim() && url.trim() && !loading;

  const handleGenerate = async () => {
    if (!canSubmit) return;
    setLoading(true);
    setError(null);
    setOutput("");

    abortRef.current?.abort();
    const ctrl = new AbortController();
    abortRef.current = ctrl;

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ company_name: company, url, model }),
        signal: ctrl.signal,
      });

      if (!res.ok) throw new Error(`Request failed (${res.status})`);
      if (!res.body) {
        const text = await res.text();
        setOutput(text);
        return;
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let acc = "";
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        acc += decoder.decode(value, { stream: true });
        setOutput(acc);
        requestAnimationFrame(() => {
          if (contentRef.current) {
            contentRef.current.scrollTop =
              contentRef.current.scrollHeight;
          }
        });

      }
      setCompany("")
      setUrl("")
    } catch (e) {
      if ((e as Error).name === "AbortError") return;
      setError(
        (e as Error).message +
        " — make sure your Python backend is running and CORS is enabled.",
      );
    } finally {
      setLoading(false);
    }
  };


const handleCopy = async () => {
  try {
    await navigator.clipboard.writeText(output);
    setCopied(true);

    setTimeout(() => {
      setCopied(false);
    }, 2000);
  } catch (err) {
    console.error(err);
  }
};

  const fillExample = (ex: (typeof EXAMPLES)[number]) => {
    setCompany(ex.name);
    setUrl(ex.url);
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="mx-auto flex max-w-5xl items-center justify-between px-6 py-5">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <Sparkles className="h-4 w-4" />
          </div>
          <span className="text-sm font-semibold tracking-tight">Brochure Generator</span>
        </div>
         <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-border bg-card px-4 py-1.5 text-xs text-muted-foreground shadow-soft">
          <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
          Powered by multi-model AI
        </div>

        {/* <h1 className="text-center text-5xl font-semibold tracking-tight text-foreground sm:text-6xl">
          Got a company in mind?
        </h1> */}

        <a
          href="https://github.com"
          className="text-sm text-muted-foreground transition-colors hover:text-foreground"
        >
          Docs
        </a>
      </header>

      <main className="mx-auto flex max-w-5xl flex-col items-center px-6 pb-24 pt-10 sm:pt-20">
       
        <p className="mt-4 max-w-xl text-center text-base text-muted-foreground">
          Drop a name and a URL — we'll read the landing page and write a clean,
          investor-ready brochure in seconds.
        </p>
         {(output || loading) && (
          // <article className="mt-12 w-full rounded-3xl border border-border bg-card p-8 shadow-soft">
          <article className="mt-12 w-full rounded-3xl border border-border bg-card shadow-soft overflow-hidden">
            <div className="flex items-center justify-between border-b border-border px-6 py-4">
              <h2 className="text-sm font-medium text-muted-foreground">
                {company ? `Brochure — ${company}` : "Brochure"}
              </h2>
              {loading && (
                <span className="flex items-center gap-2 text-xs text-muted-foreground">
                  <Loader2 className="h-3 w-3 animate-spin" /> Generating…
                </span>
              )}
              {!loading && output && (
               <button
  onClick={handleCopy}
  className="rounded-lg border border-border px-3 py-1 text-xs hover:bg-accent"
>
  {copied ? "Copied ✓" : "Copy"}
</button>
              )}
            </div>
            <div
              ref={contentRef}
              className="
              max-h-[600px]
              overflow-y-auto
              px-6
              py-5
              prose
              prose-neutral
              max-w-none
              prose-headings:tracking-tight
              prose-h1:text-3xl
              prose-h2:text-xl
              prose-a:text-foreground
              prose-strong:text-foreground
            "
            >
              <ReactMarkdown>
                {output || "_Reading the landing page..._"}
              </ReactMarkdown>
            </div>
            {/* <div className="prose prose-neutral max-w-none prose-headings:tracking-tight prose-h1:text-3xl prose-h2:text-xl prose-a:text-foreground prose-strong:text-foreground">
              <ReactMarkdown>{output || "_Reading the landing page…_"}</ReactMarkdown>
            </div> */}
          </article>
        )}
              <div className="fixed bottom-0 left-0 right-0 z-50 ">
  <div className="mx-auto max-w-3xl px-4 ">
        <div className="w-full rounded-3xl border border-border bg-card p-2 shadow-soft">
          <div className="grid gap-2 sm:grid-cols-2">
            <input
              type="text"
              placeholder="Company name"
              value={company}
              onChange={(e) => setCompany(e.target.value)}
              className="w-full rounded-2xl bg-transparent px-4 py-3 text-sm outline-none placeholder:text-muted-foreground"
            />
            <input
              type="url"
              placeholder="https://company.com"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="w-full rounded-2xl bg-transparent px-4 py-3 text-sm outline-none placeholder:text-muted-foreground"
            />
          </div>

          <div className="flex items-center justify-between gap-2 border-t border-border px-2 pt-2">
            <select
              value={model}
              onChange={(e) => setModel(e.target.value)}
              className="cursor-pointer rounded-full bg-secondary px-3 py-1.5 text-xs font-medium text-secondary-foreground outline-none transition-colors hover:bg-accent"
            >
              {MODELS.map((m) => (
                <option key={m.value} value={m.value}>
                  {m.label}
                </option>
              ))}
            </select>

            <button
              onClick={handleGenerate}
              disabled={!canSubmit}
              className="flex h-9 w-9 items-center justify-center rounded-full bg-primary text-primary-foreground transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-40"
              aria-label="Generate brochure"
            >
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <ArrowUp className="h-4 w-4" />
              )}
            </button>
          </div>
        </div>

        {/* <div className="mt-6 flex flex-wrap items-center justify-center gap-2">
          <span className="text-xs text-muted-foreground">Try:</span>
          {EXAMPLES.map((ex) => (
            <button
              key={ex.name}
              onClick={() => fillExample(ex)}
              className="rounded-full border border-border bg-card px-3 py-1 text-xs text-foreground transition-colors hover:bg-accent"
            >
              {ex.name}
            </button>
          ))}
        </div> */}

        {error && (
          <div className="mt-8 w-full rounded-2xl border border-destructive/30 bg-destructive/5 px-5 py-4 text-sm text-destructive">
            {error}
          </div>
        )}
       </div>
       </div>
       
      </main>

      {/* <footer className="mx-auto max-w-5xl px-6 pb-10 text-center text-xs text-muted-foreground">
        Built by Sreekanth
      </footer> */}
    </div>
  );
}
