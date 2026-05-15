# QuickAdd Macro: Voice Capture → Daily Note

This is a **template guide** for setting up a QuickAdd macro that takes a voice memo file, transcribes it via your existing ElevenLabs MCP (through Claude Code), and appends the transcript to today's daily note in `obsidian-claude`.

## Dependencies

- **QuickAdd plugin** (chhoumann, 2,209 stars, active): install in Obsidian
- **Templater plugin** (SilentVoid13, 4,933 stars, active): install in Obsidian
- **Claude Code** installed and accessible from PATH
- **ElevenLabs MCP** already configured at `~/.claude.json` (verified present in user's config)

## Two implementation paths

### Path A: recommended (Claude Code shells out to ElevenLabs MCP)

QuickAdd macro chain:
1. **UserScript: pickVoiceFile**: file picker for `.m4a/.mp3/.wav` returning filepath
2. **UserScript: transcribeVoice**: invokes Claude Code with prompt to transcribe via ElevenLabs MCP
3. **Capture**: appends transcript to `Daily Notes/{{date:YYYY-MM-DD}}.md` under `## Voice memo {{time:HH:mm}}` heading

### Path B: standalone (Templater calls ElevenLabs API directly)

Same chain but step 2 calls ElevenLabs API direct: requires API key in Templater settings (already in Proton Pass as `ElevenLabs Claude Code` per user's setup).

## User-function templates

Save these in a **vault-root folder** (e.g., `~/obsidian-claude/scripts/`), **NOT inside `.obsidian/`**. QuickAdd v2.x explicitly rejects scripts inside `.obsidian/` (verified 2026-05-15 against `chhoumann/quickadd:src/gui/MacroGUIs/noScriptsFoundNotice.ts` — the error message says: "In your vault (not in .obsidian folder), Not in hidden folders (starting with a dot), Have a .js extension"). Templater scripts CAN live inside `.obsidian/scripts/`, but QuickAdd User Script steps cannot. If you want both Templater and QuickAdd to use the same `.js`, put it at the vault root.

### `pickVoiceFile.js`

```javascript
// Templater user function: open file picker for voice memos
async function pickVoiceFile(tp) {
  const path = await tp.system.suggester(
    (file) => file.path,
    app.vault.getFiles().filter(f =>
      ['m4a', 'mp3', 'wav', 'ogg'].includes(f.extension)
    )
  );
  return path?.path || null;
}
module.exports = pickVoiceFile;
```

### `transcribeVoice.js` (Path A: uses execFile, not exec)

```javascript
// Templater user function: invoke Claude Code with ElevenLabs MCP for transcription.
// Uses execFile (NOT exec) to prevent command injection per user CLAUDE.md security guidance.
async function transcribeVoice(filepath) {
  const { execFile } = require('child_process');
  const { promisify } = require('util');
  const execFileAsync = promisify(execFile);

  // Validate filepath (defensive: Templater context but be safe)
  if (!filepath || typeof filepath !== 'string') {
    throw new Error('transcribeVoice: filepath required');
  }

  const prompt = `use elevenlabs MCP to transcribe ${filepath} and return only the transcript text, no commentary, no markdown formatting`;

  // execFile takes program + arg array: no shell, no injection.
  const { stdout } = await execFileAsync('claude-code', ['--prompt', prompt], {
    maxBuffer: 10 * 1024 * 1024,  // 10 MB transcript ceiling
    timeout: 120000,                // 2 min cap
  });

  return stdout.trim();
}
module.exports = transcribeVoice;
```

## QuickAdd macro configuration (set in plugin GUI; v2.x verified 2026-05-15 against `chhoumann/quickadd:src/gui/choiceList/AddChoiceBox.svelte`)

1. Open Obsidian, Settings, QuickAdd. There's no "Manage Macros" page in v2.x; macros are added as a Choice TYPE.
2. In the top "Choices and Packages" section: type **Voice Capture** in the Name field.
3. Click the type-selector dropdown (HTML `<select>`, defaults to displaying "Template") next to the Name field. The 4 options are Template, Capture, Macro, Multi. Pick **Macro**.
4. Click **Add Choice** (the purple `mod-cta` button). The macro appears in the choice list above.
5. Click the gear/settings icon next to "Voice Capture" in the choice list to open the macro configurator.
6. Inside the configurator, add steps in order:
   1. **Add, User Script** then select `pickVoiceFile` from the file picker.
   2. **Add, User Script** then select `transcribeVoice`.
   3. **Add, Capture** with these settings:
      - **File path / format:** match your daily-notes setup (check Obsidian Settings, Daily notes, "New file location"). For vault-root daily notes use `{{DATE:YYYY-MM-DD}}.md`. For a subfolder use `<your-folder>/{{DATE:YYYY-MM-DD}}.md`. Variable names ARE case-sensitive: uppercase `{{DATE}}` and `{{VALUE}}` are canonical (verified 2026-05-15 against `chhoumann/quickadd:src/formatters/fileNameDisplayFormatter.test.ts`).
      - **Create file if it doesn't exist:** ON
      - **Position, Write position:** Bottom of file (so memos append, not push down existing content)
      - **Capture format:** ON
      - **Format textarea:**
        ```
        
        ## Voice memo {{DATE:HH:mm}}
        
        {{VALUE}}
        
        ```
4. Bind to ribbon icon or hotkey (e.g., `Ctrl+Alt+V`)

## Testing checklist (Wave 4 empirical validation)

- [ ] Place a `.m4a` voice memo in `obsidian-claude/Audio/`
- [ ] Trigger Voice Capture macro
- [ ] File picker shows the memo
- [ ] Transcription completes within 2 minutes
- [ ] Transcript appended to today's daily note under correct heading
- [ ] No errors in DevTools console
- [ ] Source filepath included in append for traceability

## Known caveats

- ElevenLabs MCP must be reachable from Claude Code's environment: confirmed present in `~/.claude.json`
- 2-minute timeout is conservative for ElevenLabs Scribe v2; bump if your memos are >30 min
- Transcript is appended as-is; for cleanup (filler removal, paragraph breaks), chain a second Claude Code call

## Status

**TEMPLATE: install Phase 4 of `SOTA-PROPOSAL-v3.md` rollout.** Empirical validation pending Wave 4. The user runs this once on `obsidian-claude`, verifies, then commits the working `.js` files to the vault git repo for portability.
