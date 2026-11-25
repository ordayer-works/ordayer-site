// Keeps the computer responsive while several Claude sessions, the editor and a browser share its
// memory. Before a session starts something heavy (a dev server, Docker, a whole build or test run,
// a test browser), this reads how much memory is available and refuses while it is below the
// floor, so one session cannot push the rest into swapping. A PreToolUse hook in
// .claude/settings.json: exit code 2 refuses and hands Claude the message. Any error lets the step
// through, since a broken guard must never stop work. It sets the exit code rather than calling
// process.exit, which can cut the message short where writing to a pipe is asynchronous (macOS).
import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { freemem } from "node:os";
import { floorOf, fromMeminfo, fromVmStat, isHeavy, refusal } from "./ram-guard-rules.mjs";

function availableBytes() {
  if (process.platform === "darwin") {
    return fromVmStat(execFileSync("/usr/bin/vm_stat", { encoding: "utf8", timeout: 2000 }));
  }
  if (process.platform === "linux") return fromMeminfo(readFileSync("/proc/meminfo", "utf8"));
  // Windows counts memory on standby as available, which is what it hands out without paging.
  return freemem();
}

try {
  const input = JSON.parse(readFileSync(0, "utf8"));
  const tool = String(input?.tool_name ?? "");
  if (isHeavy(tool, String(input?.tool_input?.command ?? ""))) {
    const bytes = availableBytes();
    const gb = bytes === null ? null : bytes / 2 ** 30;
    // biome-ignore lint/suspicious/noUndeclaredEnvVars: a Claude Code hook reads this, not a Turborepo task.
    const floor = floorOf(process.env.RAM_GUARD_FLOOR_GB);
    if (gb !== null && gb < floor) {
      console.error(refusal(tool, gb));
      process.exitCode = 2;
    }
  }
} catch {
  // Unreadable input or memory figures: let the step through.
}
