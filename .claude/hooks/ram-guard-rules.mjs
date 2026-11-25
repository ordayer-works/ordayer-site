// What ram-guard.mjs decides, as plain functions, so a test can check each one on any computer.
// The same two files sit in every ordayer-works repo, and the repos with a test suite check them in
// scripts/ram-guard.test.mjs.

// Below this much available memory a computer starts swapping hard and every open window stalls.
const FLOOR_GB = 1.5;

// Flags may sit between a tool and its command, as in `pnpm --filter web build`.
const FLAGS = String.raw`(\s+-[\w-]+(=\S+|\s+[^\s;&|-]\S*)?)*`;
const RUNNER = String.raw`\b(pnpm|npm|yarn|bun)${FLAGS}\s+(run\s+)?`;

// Commands that start something holding hundreds of MB to a few GB while it runs.
const HEAVY = [
  /\b(next|vite|astro|nuxt)\s+(dev|build|start)\b/,
  new RegExp(String.raw`${RUNNER}(dev|start|build|preview|verify|check)\b`),
  new RegExp(String.raw`${RUNNER}test\s*($|[;&|])`),
  /\bturbo\s+(run\s+)?\w/,
  new RegExp(String.raw`\bdocker(\s+compose|-compose)?${FLAGS}\s+(up|run|start)\b`),
  /\bplaywright\s+test\b/,
];

const BROWSER = "mcp__playwright__browser_navigate";

/** Whether this step starts something heavy. RAM_GUARD=off in the command lets it through. */
export function isHeavy(tool, command) {
  if (tool === BROWSER) return true;
  if (tool !== "Bash" && tool !== "PowerShell") return false;
  return !/RAM_GUARD\W{0,3}off/i.test(command) && HEAVY.some((re) => re.test(command));
}

/** The floor in GB: RAM_GUARD_FLOOR_GB in the environment Claude Code runs in, if it is a number. */
export function floorOf(setting) {
  const gb = Number(setting);
  return setting !== undefined && setting !== "" && Number.isFinite(gb) && gb >= 0 ? gb : FLOOR_GB;
}

/** Available bytes on macOS from vm_stat: pages free, inactive and speculative, which macOS hands
 *  out without swapping. Node's own figure there counts only the free ones, often near nothing. */
export function fromVmStat(text) {
  const page = Number(/page size of (\d+) bytes/.exec(text)?.[1]);
  const pages = (name) =>
    Number(new RegExp(String.raw`^Pages ${name}:\s+(\d+)\.`, "m").exec(text)?.[1]);
  const bytes = page * (pages("free") + pages("inactive") + pages("speculative"));
  return Number.isFinite(bytes) ? bytes : null;
}

/** Available bytes on Linux, as the kernel estimates them (MemAvailable in /proc/meminfo). */
export function fromMeminfo(text) {
  const kb = Number(/^MemAvailable:\s+(\d+)\s+kB/m.exec(text)?.[1]);
  return Number.isFinite(kb) ? kb * 1024 : null;
}

/** What Claude reads when a step is refused: why, and what to do instead. */
export function refusal(tool, availableGb) {
  return [
    `[ramGuard] Only ${availableGb.toFixed(1)} GB of memory is free on this computer, and other Claude sessions, the editor and the browser share it.`,
    "Starting this now would slow everything down.",
    "Stop a dev server, test browser or Docker container this session started and no longer needs, or wait a few minutes and try again.",
    tool === BROWSER
      ? ""
      : "Only if the person says to go ahead anyway, add RAM_GUARD=off to the command.",
  ]
    .filter(Boolean)
    .join(" ");
}
