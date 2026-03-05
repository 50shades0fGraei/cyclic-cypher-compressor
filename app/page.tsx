import { ConverterPanel } from "@/components/converter-panel"

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center px-4 py-16 sm:py-24">
      {/* Header */}
      <header className="flex flex-col items-center gap-3 text-center">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-md bg-[hsl(var(--primary))]">
            <span className="font-mono text-xs font-bold text-[hsl(var(--primary-foreground))]">
              CC
            </span>
          </div>
          <h1 className="text-balance text-2xl font-bold tracking-tight text-[hsl(var(--foreground))] sm:text-3xl">
            Cyclic Cypher Compressor
          </h1>
        </div>
        <p className="max-w-md text-pretty text-sm leading-relaxed text-[hsl(var(--muted-foreground))]">
          Lossless file compression using the CCC2 binary format.
          Convert any file to <code className="font-mono text-[hsl(var(--primary))]">.cc</code> or
          restore it back to the original.
        </p>
      </header>

      {/* Converter */}
      <section className="mt-10 flex w-full justify-center sm:mt-14">
        <ConverterPanel />
      </section>

      {/* Footer */}
      <footer className="mt-auto pt-16">
        <p className="text-xs text-[hsl(var(--muted-foreground))]">
          All processing happens client-side. Files never leave your browser.
        </p>
      </footer>
    </main>
  )
}
