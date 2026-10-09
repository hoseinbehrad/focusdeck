# CSS module for FocusDeck
CSS_CONTENT = """
:root {
  --bg:        #070A16;
  --surface:   #111629;
  --surface-2: #0C1120;
  --border:    rgba(255,255,255,0.06);
  --border-focus: rgba(79,91,240,0.5);
  --text:      #E8EAF6;
  --muted:     #7A83A6;
  --accent:    #4F5BF0;
  --accent-2:  #7C5CFF;
  --teal:      #2DD4A7;
  --coral:     #FF5C6C;
  --amber:     #FFB648;
  --gold-deep: #D97706;
  --pink:      #FF4FA3;
  --font:      -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --radius-card: 20px;
  --radius-btn: 10px;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  background-color: var(--bg);
  color: var(--text);
  font-family: var(--font);
  min-height: 100vh;
  overflow-x: hidden;
  font-size: 14px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

/* Custom Scrollbars */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: var(--surface-2);
}
::-webkit-scrollbar-thumb {
  background: rgba(255,255,255,0.15);
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: rgba(255,255,255,0.25);
}

/* App Container Layout */
#app-container {
  display: flex;
  min-height: 100vh;
  width: 100%;
}

/* =========================================
   1. SIDEBAR (FIXED 220px)
   ========================================= */
#sidebar {
  width: 220px;
  flex-shrink: 0;
  background-color: var(--surface-2);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  padding: 24px 16px;
  position: sticky;
  top: 0;
  height: 100vh;
  z-index: 100;
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 8px 24px 8px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 20px;
}

.brand-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(79,91,240,0.3);
}

.brand-name {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.5px;
  color: #fff;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: var(--radius-btn);
  color: var(--muted);
  cursor: pointer;
  transition: all 200ms ease;
  font-weight: 500;
  user-select: none;
  background: transparent;
  border: none;
  width: 100%;
  text-align: left;
}

.nav-item:hover {
  color: var(--text);
  background-color: rgba(255,255,255,0.03);
}

.nav-item.active {
  color: #fff;
  background-color: var(--surface);
  border: 1px solid var(--border);
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.nav-item svg {
  width: 18px;
  height: 18px;
  stroke: currentColor;
  stroke-width: 1.75;
  fill: none;
  flex-shrink: 0;
}

.sidebar-bottom {
  border-top: 1px solid var(--border);
  padding-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.streak-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.streak-info {
  display: flex;
  flex-direction: column;
}

.streak-label {
  font-size: 11px;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.streak-val {
  font-size: 16px;
  font-weight: 700;
  color: var(--amber);
  display: flex;
  align-items: center;
  gap: 4px;
}

.daily-goal-prog {
  margin-top: 6px;
}

.prog-bar-bg {
  height: 5px;
  background: rgba(255,255,255,0.08);
  border-radius: 3px;
  overflow: hidden;
  margin-top: 4px;
}

.prog-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent), var(--teal));
  border-radius: 3px;
  width: 0%;
  transition: width 300ms ease;
}

/* =========================================
   2. CONTENT LAYOUT (FLEX 1)
   ========================================= */
#main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  overflow-y: auto;
  height: 100vh;
}

.view-container {
  display: none;
  padding: 28px 36px;
  max-width: 1600px;
  margin: 0 auto;
  width: 100%;
}

.view-container.active {
  display: block;
}

/* Common Card Styles */
.card {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  box-shadow: 0 8px 24px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.07);
  padding: 24px;
  position: relative;
}

/* Headers */
.view-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  gap: 16px;
  flex-wrap: wrap;
}

.view-title {
  font-size: 24px;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.5px;
}

.view-desc {
  font-size: 13px;
  color: var(--muted);
  margin-top: 2px;
}

/* =========================================
   3. VIEW 1: TIMER DASHBOARD
   ========================================= */
.timer-view-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 380px;
  gap: 28px;
  align-items: start;
}

@media (max-width: 1100px) {
  .timer-view-grid {
    grid-template-columns: 1fr;
  }
}

.timer-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 40px 32px 32px 32px;
  position: relative;
  overflow: hidden;
  transition: all 400ms ease;
}

.timer-card.running {
  background: radial-gradient(circle at 50% 30%, #171d3a 0%, #111629 80%);
  border-color: rgba(79,91,240,0.25);
  box-shadow: 0 12px 36px rgba(0,0,0,0.4), 0 0 60px rgba(79,91,240,0.12), inset 0 1px 0 rgba(255,255,255,0.1);
}

.mode-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: 20px;
  background: rgba(255,255,255,0.05);
  border: 1px solid var(--border);
  color: var(--text);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  margin-bottom: 24px;
}

.timer-dial-wrap {
  position: relative;
  width: 280px;
  height: 280px;
  margin: 0 auto 24px auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

.timer-svg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.timer-ring-bg {
  fill: none;
  stroke: rgba(255,255,255,0.05);
  stroke-width: 8;
}

.timer-ring-circle {
  fill: none;
  stroke: url(#timerGradient);
  stroke-width: 8;
  stroke-linecap: round;
  stroke-dasharray: 741.42;
  stroke-dashoffset: 0;
  transition: stroke-dashoffset 250ms linear;
}

.timer-center-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.timer-digits {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 68px;
  font-weight: 700;
  color: #fff;
  letter-spacing: -2px;
  line-height: 1;
  text-shadow: 0 4px 16px rgba(0,0,0,0.4);
}

.timer-cycle-dots {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 14px;
}

.timer-cycle-dots .dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255,255,255,0.15);
  transition: all 200ms ease;
}

.timer-cycle-dots .dot.filled {
  background: var(--teal);
  box-shadow: 0 0 8px rgba(45,212,167,0.5);
}

.timer-cycle-dots .dot.active {
  background: var(--accent);
  box-shadow: 0 0 8px rgba(79,91,240,0.6);
  transform: scale(1.25);
}

/* The Wave Band */
.wave-band-container {
  width: 100%;
  height: 52px;
  position: relative;
  overflow: hidden;
  margin: 10px 0 24px 0;
  opacity: 0.9;
}

.wave-band-container svg {
  width: 200%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
}

.wave-path {
  transition: d 400ms ease, opacity 400ms ease;
}

.wave-running .wave-1 {
  animation: waveScroll 5s linear infinite;
}
.wave-running .wave-2 {
  animation: waveScroll 8s linear infinite reverse;
}
.wave-running .wave-3 {
  animation: waveScroll 11s linear infinite;
}

.wave-paused svg {
  animation-play-state: paused !important;
  opacity: 0.35;
  filter: grayscale(80%);
}

.wave-idle svg {
  animation: none !important;
  opacity: 0.2;
}

@keyframes waveScroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

@media (prefers-reduced-motion: reduce) {
  .wave-running svg {
    animation: none !important;
  }
}

/* Task & Tag Input */
.task-binder-row {
  width: 100%;
  max-width: 480px;
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.task-input-wrapper {
  position: relative;
  width: 100%;
}

.task-input {
  width: 100%;
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--radius-btn);
  padding: 12px 16px;
  color: #fff;
  font-size: 15px;
  font-family: inherit;
  outline: none;
  transition: border-color 200ms ease, box-shadow 200ms ease;
}

.task-input:focus {
  border-color: var(--border-focus);
  box-shadow: 0 0 0 3px rgba(79,91,240,0.2);
}

.task-input::placeholder {
  color: var(--muted);
}

.tags-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  justify-content: center;
}

.chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 14px;
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border);
  color: var(--muted);
  font-size: 12px;
  cursor: pointer;
  transition: all 150ms ease;
  user-select: none;
}

.chip:hover {
  background: rgba(255,255,255,0.08);
  color: var(--text);
}

.chip.selected {
  background: rgba(79,91,240,0.15);
  border-color: var(--accent);
  color: #fff;
}

.chip-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

/* Timer Controls */
.timer-controls {
  display: flex;
  align-items: center;
  gap: 14px;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: var(--radius-btn);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all 150ms ease;
  user-select: none;
  font-family: inherit;
  text-decoration: none;
}

.btn-primary {
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  color: #fff;
  padding: 14px 36px;
  font-size: 16px;
  box-shadow: 0 4px 16px rgba(79,91,240,0.35);
}

.btn-primary:hover {
  box-shadow: 0 6px 22px rgba(79,91,240,0.5);
  transform: translateY(-1px);
}

@keyframes pulse-idle-subtle {
  0% {
    box-shadow: 0 4px 16px rgba(79, 91, 240, 0.35);
    transform: scale(1);
  }
  50% {
    box-shadow: 0 4px 26px rgba(79, 91, 240, 0.75), 0 0 0 5px rgba(79, 91, 240, 0.22);
    transform: scale(1.025);
  }
  100% {
    box-shadow: 0 4px 16px rgba(79, 91, 240, 0.35);
    transform: scale(1);
  }
}

.btn-pulse-idle {
  animation: pulse-idle-subtle 2.2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}

.btn-secondary {
  background: rgba(255,255,255,0.06);
  border-color: var(--border);
  color: var(--text);
}

.btn-secondary:hover {
  background: rgba(255,255,255,0.1);
  color: #fff;
}

.btn-danger {
  background: rgba(255,92,108,0.12);
  border-color: rgba(255,92,108,0.3);
  color: var(--coral);
}

.btn-danger:hover {
  background: rgba(255,92,108,0.22);
}

.btn-sm {
  padding: 6px 12px;
  font-size: 12px;
}

.btn svg {
  width: 16px;
  height: 16px;
  stroke: currentColor;
  stroke-width: 2;
  fill: none;
}

/* Right Column Panels */
.right-column-stack {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.stats-grid-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.stat-card {
  background: #0E1322;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 16px 14px 14px 16px;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  min-height: 86px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.stat-card-label {
  font-size: 11px;
  font-weight: 700;
  color: #727E9E;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  margin-bottom: 8px;
}

.stat-card-value {
  font-size: 24px;
  font-weight: 800;
  color: #FFFFFF;
  letter-spacing: -0.5px;
  line-height: 1;
  z-index: 1;
}

.stat-card-val-coral {
  color: #FF5C6C !important;
}

.stat-card-corner {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 62px;
  height: 38px;
  pointer-events: none;
}

/* Recent Sessions Card */
.recent-sessions-card {
  background: #0E1322;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 22px 20px 24px 20px;
  display: flex;
  flex-direction: column;
  min-height: 440px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
}

.recent-sessions-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 18px;
}

.recent-sessions-title {
  font-size: 16px;
  font-weight: 700;
  color: #FFFFFF;
  letter-spacing: -0.2px;
}

.recent-sessions-subtitle {
  font-size: 12px;
  font-weight: 500;
  color: #64748B;
  margin-top: 3px;
}

.recent-sessions-view-all {
  background: none;
  border: none;
  font-family: inherit;
  font-size: 13px;
  font-weight: 600;
  color: #727E9E;
  cursor: pointer;
  padding: 2px 4px;
  transition: color 150ms ease;
}

.recent-sessions-view-all:hover {
  color: #FFFFFF;
}

.recent-sessions-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.recent-session-card {
  background: #14192E;
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 12px;
  padding: 12px 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  transition: background 150ms ease, border-color 150ms ease, transform 150ms ease;
  cursor: default;
}

.recent-session-card:hover {
  background: #181E38;
  border-color: rgba(255, 255, 255, 0.08);
  transform: translateY(-1px);
}

.recent-session-left {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.recent-session-avatar {
  width: 38px;
  height: 38px;
  min-width: 38px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 800;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  letter-spacing: 0.5px;
}

.recent-session-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.recent-session-name {
  font-size: 14px;
  font-weight: 700;
  color: #FFFFFF;
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 170px;
}

.recent-session-type {
  font-size: 12px;
  font-weight: 500;
  color: #727E9E;
  margin-top: 2px;
  line-height: 1.2;
}

.recent-session-right {
  text-align: right;
  flex-shrink: 0;
}

.recent-session-dur {
  font-size: 13px;
  font-weight: 700;
  color: #FFFFFF;
}

.recent-session-time {
  font-size: 12px;
  font-weight: 500;
  color: #64748B;
  margin-top: 2px;
}

.recent-empty-state {
  font-size: 12px;
  color: #64748B;
  padding: 24px 0;
  text-align: center;
}

.icon-btn-sm {
  background: transparent;
  border: none;
  color: var(--muted);
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
}

.icon-btn-sm:hover {
  color: #fff;
  background: rgba(255,255,255,0.1);
}

.icon-btn-sm svg {
  width: 14px;
  height: 14px;
  stroke: currentColor;
  stroke-width: 2;
  fill: none;
}

/* Parked thoughts */
.thought-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  border-radius: 8px;
  background: rgba(255,255,255,0.02);
  border: 1px solid var(--border);
  font-size: 13px;
  margin-bottom: 6px;
}

.thought-item.cleared {
  opacity: 0.5;
  text-decoration: line-through;
}

/* =========================================
   4. VIEW: TIME BLOCK (NEW)
   ========================================= */
.tb-container {
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

@media (max-width: 1080px) {
  .tb-container {
    flex-direction: column;
  }
}

.tb-builder-panel {
  width: 340px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.tb-timeline-panel {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Time Block Header Controls */
.tb-date-nav {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--surface-2);
  padding: 4px 8px;
  border-radius: 10px;
  border: 1px solid var(--border);
}

.tb-date-weekday {
  font-size: 13px;
  font-weight: 600;
  color: var(--muted);
  padding: 0 4px;
  display: inline-block;
}

.recent-session-actions {
  display: flex;
  align-items: center;
  gap: 2px;
}

.recent-session-actions .icon-btn-sm {
  padding: 4px 5px;
  border-radius: 6px;
  opacity: 0.75;
  transition: opacity 150ms, color 150ms, background 150ms;
}

.recent-session-actions .icon-btn-sm:hover {
  opacity: 1;
}

.tb-daywindow-controls {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--muted);
}

.tb-time-input {
  background: var(--surface);
  border: 1px solid var(--border);
  color: #fff;
  padding: 4px 8px;
  border-radius: 6px;
  font-family: inherit;
  font-size: 12px;
}

/* Block builder list */
.tb-blocks-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 520px;
  overflow-y: auto;
  padding-right: 4px;
}

.tb-block-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  border-radius: 8px;
  background: var(--surface-2);
  border: 1px solid var(--border);
  transition: all 150ms ease;
  user-select: none;
}

.tb-block-row:hover {
  border-color: rgba(255,255,255,0.12);
}

.tb-block-row.dragging {
  opacity: 0.4;
}

.tb-drag-handle {
  cursor: grab;
  color: var(--muted);
  display: flex;
  align-items: center;
}

.tb-drag-handle:active {
  cursor: grabbing;
}

.tb-color-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.tb-row-label {
  flex: 1;
  background: transparent;
  border: none;
  color: #fff;
  font-size: 13px;
  font-family: inherit;
  min-width: 0;
  outline: none;
}

.tb-row-label:focus {
  border-bottom: 1px solid var(--accent);
}

.tb-row-dur {
  width: 44px;
  background: rgba(255,255,255,0.05);
  border: 1px solid var(--border);
  border-radius: 4px;
  color: var(--text);
  font-size: 12px;
  text-align: center;
  padding: 2px 4px;
  font-family: inherit;
}

/* Sticky Note / Scratchpad in Time Block Panel */
.tb-sticky-note-card {
  position: relative;
  background: linear-gradient(175deg, #1B1812 0%, #131317 100%);
  border: 1px solid rgba(245, 158, 11, 0.22);
  border-top: 3px solid #F59E0B;
  box-shadow: 0 10px 28px rgba(0,0,0,0.35), 0 0 20px rgba(245, 158, 11, 0.05);
  padding: 20px 16px 14px 16px;
  border-radius: var(--radius-card);
  transition: border-color 200ms ease, box-shadow 200ms ease;
}

.tb-sticky-note-card:hover {
  border-color: rgba(245, 158, 11, 0.35);
  box-shadow: 0 12px 32px rgba(0,0,0,0.4), 0 0 24px rgba(245, 158, 11, 0.08);
}

.tb-sticky-note-tape {
  position: absolute;
  top: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 56px;
  height: 15px;
  background: rgba(245, 158, 11, 0.24);
  border: 1px solid rgba(245, 158, 11, 0.45);
  backdrop-filter: blur(4px);
  border-radius: 2px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.25);
  pointer-events: none;
}

.tb-sticky-note-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 4px;
}

.tb-sticky-note-title {
  font-size: 13px;
  font-weight: 700;
  color: #FDE68A;
  letter-spacing: -0.2px;
}

.tb-sticky-save-status {
  font-size: 11px;
  color: rgba(251, 191, 36, 0.7);
  font-weight: 500;
  transition: opacity 200ms ease;
}

.tb-sticky-note-sub {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.45);
  margin-bottom: 10px;
  line-height: 1.35;
}

.tb-sticky-note-textarea {
  width: 100%;
  min-height: 130px;
  max-height: 280px;
  resize: vertical;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(245, 158, 11, 0.16);
  border-radius: 8px;
  padding: 10px 12px;
  color: #FEF3C7;
  font-family: inherit;
  font-size: 13px;
  line-height: 1.55;
  outline: none;
  transition: border-color 150ms ease, box-shadow 150ms ease;
}

.tb-sticky-note-textarea::placeholder {
  color: rgba(253, 230, 138, 0.35);
  font-size: 12px;
  line-height: 1.45;
}

.tb-sticky-note-textarea:focus {
  border-color: rgba(245, 158, 11, 0.55);
  box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.12);
}

.tb-sticky-note-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 10px;
  padding-top: 8px;
  border-top: 1px dashed rgba(245, 158, 11, 0.15);
}

/* Timeline Canvas */
.tb-timeline-card {
  padding: 0;
  overflow: hidden;
}

.tb-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 20px;
  border-bottom: 1px solid var(--border);
  background: rgba(255,255,255,0.01);
  flex-wrap: wrap;
  gap: 10px;
}

.tb-timeline-scroll {
  position: relative;
  overflow-y: auto;
  max-height: 680px;
  min-height: 520px;
  padding: 20px 20px 20px 65px;
}

.tb-hour-labels {
  position: absolute;
  top: 20px;
  left: 10px;
  width: 48px;
  bottom: 20px;
  pointer-events: none;
}

.tb-hour-label {
  position: absolute;
  font-size: 11px;
  color: var(--muted);
  font-family: ui-monospace, SFMono-Regular, monospace;
  transform: translateY(-50%);
  text-align: right;
  width: 100%;
}

.tb-track {
  position: relative;
  width: 100%;
  border-left: 1px solid var(--border);
}

.tb-hour-gridline {
  position: absolute;
  left: 0;
  right: 0;
  height: 1px;
  background: rgba(255,255,255,0.06);
  pointer-events: none;
}

.tb-halfhour-gridline {
  position: absolute;
  left: 0;
  right: 0;
  height: 1px;
  border-top: 1px dashed rgba(255,255,255,0.03);
  pointer-events: none;
}

/* Visual Block Rect */
.tb-block-item {
  position: absolute;
  left: 12px;
  right: 12px;
  border-radius: 10px;
  border: 1px solid rgba(255,255,255,0.12);
  padding: 8px 12px;
  cursor: grab;
  overflow: hidden;
  transition: box-shadow 150ms ease, transform 150ms ease;
  box-shadow: 0 4px 14px rgba(0,0,0,0.3);
  z-index: 2;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.tb-block-item:hover {
  z-index: 5;
  box-shadow: 0 6px 20px rgba(0,0,0,0.5);
}

.tb-block-item.is-moving {
  cursor: grabbing;
  z-index: 10;
  opacity: 0.9;
}

.tb-block-item.inProgress {
  animation: tbPulse 2s infinite ease-in-out;
  border-color: var(--accent);
}

@keyframes tbPulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(79,91,240,0.4); }
  50% { box-shadow: 0 0 18px 2px rgba(79,91,240,0.7); }
}

.tb-block-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
}

.tb-block-title {
  font-weight: 700;
  font-size: 13px;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tb-block-time {
  font-size: 11px;
  font-family: ui-monospace, SFMono-Regular, monospace;
  opacity: 0.85;
}

.tb-block-resize-handle {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 7px;
  cursor: ns-resize;
  background: transparent;
  transition: background 150ms ease;
}

.tb-block-resize-handle:hover {
  background: rgba(255,255,255,0.25);
}

/* Actual time bar overlay on done blocks */
.tb-actual-bar {
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  width: 4px;
  border-radius: 4px 0 0 4px;
}

.tb-actual-bar.green {
  background: var(--teal);
  box-shadow: 0 0 8px rgba(45,212,167,0.5);
}

.tb-actual-bar.red {
  background: var(--coral);
  box-shadow: 0 0 8px rgba(255,92,108,0.7);
}

.tb-overrun-tail {
  position: absolute;
  left: 12px;
  right: 12px;
  background: rgba(255,92,108,0.18);
  border: 1px dashed var(--coral);
  border-radius: 0 0 10px 10px;
  pointer-events: none;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  color: var(--coral);
  font-weight: 700;
}

/* Gaps */
.tb-gap {
  position: absolute;
  left: 12px;
  right: 12px;
  border: 1px dashed rgba(255,255,255,0.08);
  background: rgba(255,255,255,0.012);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--muted);
  font-size: 12px;
  cursor: pointer;
  transition: all 150ms ease;
}

.tb-gap:hover {
  background: rgba(79,91,240,0.07);
  border-color: rgba(79,91,240,0.3);
  color: var(--text);
}

/* Now line */
.tb-now-line {
  position: absolute;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--coral);
  z-index: 8;
  pointer-events: none;
  box-shadow: 0 0 8px var(--coral);
}

.tb-now-dot {
  position: absolute;
  left: -4px;
  top: -4px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--coral);
}

/* =========================================
   5. VIEW: 10,000 HOURS (NEW)
   ========================================= */
.skills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 22px;
}

.skill-card {
  cursor: pointer;
  transition: transform 200ms ease, box-shadow 200ms ease, border-color 200ms ease;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.skill-card:hover {
  transform: translateY(-2px);
  border-color: rgba(255,182,72,0.3);
  box-shadow: 0 12px 32px rgba(0,0,0,0.4), 0 0 24px rgba(255,182,72,0.08);
}

.skill-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.skill-name-row {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.skill-name {
  font-size: 17px;
  font-weight: 700;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* THE JAR */
.jar-container {
  width: 100%;
  height: 180px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.jar-svg {
  height: 100%;
  overflow: visible;
}

.jar-celebrate {
  animation: jarPulse 700ms ease-out;
}

@keyframes jarPulse {
  0% { transform: scale(1); filter: drop-shadow(0 0 0 rgba(255,182,72,0)); }
  50% { transform: scale(1.08); filter: drop-shadow(0 0 24px rgba(255,182,72,0.9)); }
  100% { transform: scale(1); filter: drop-shadow(0 0 0 rgba(255,182,72,0)); }
}

.jar-wave-liquid {
  animation: jarLiquidWave 6s linear infinite;
}

@keyframes jarLiquidWave {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

.coin-bob {
  animation: coinFloat 3s ease-in-out infinite;
  transform-origin: center;
}

@keyframes coinFloat {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-4px) rotate(4deg); }
}

/* Skill metrics */
.skill-metrics {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.skill-total-hours {
  font-size: 32px;
  font-weight: 800;
  color: #fff;
  letter-spacing: -1px;
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.skill-backlog-badge {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 10px;
  background: rgba(255,182,72,0.15);
  color: var(--amber);
  border: 1px solid rgba(255,182,72,0.3);
  font-weight: 600;
}

.skill-subtext {
  font-size: 12px;
  color: var(--muted);
  line-height: 1.4;
}

/* Toast Notifications */
#toast-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
  pointer-events: none;
}

.toast {
  pointer-events: auto;
  background: var(--surface);
  border: 1px solid var(--amber);
  color: #fff;
  padding: 12px 18px;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.5), 0 0 20px rgba(255,182,72,0.25);
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  font-size: 13px;
  animation: toastIn 300ms ease forwards;
}

@keyframes toastIn {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

/* =========================================
   6. VIEW: LOG & REPORTS & SETTINGS
   ========================================= */
.table-card {
  padding: 0;
  overflow: hidden;
}

.log-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
  gap: 14px;
  flex-wrap: wrap;
}

.table-responsive {
  width: 100%;
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 13px;
}

.data-table th {
  padding: 12px 16px;
  background: var(--surface-2);
  color: var(--muted);
  font-weight: 600;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid var(--border);
  white-space: nowrap;
  position: sticky;
  top: 0;
  z-index: 10;
}

.data-table td {
  padding: 14px 16px;
  border-bottom: 1px solid var(--border);
  color: var(--text);
  vertical-align: middle;
}

.data-table tr:hover td {
  background: rgba(255,255,255,0.02);
}

.editable-cell {
  cursor: pointer;
  border-bottom: 1px dashed rgba(255,255,255,0.15);
  padding-bottom: 1px;
}

.editable-cell:hover {
  border-bottom-color: var(--accent);
  color: #fff;
}

.cell-input {
  background: var(--surface-2);
  border: 1px solid var(--accent);
  border-radius: 4px;
  padding: 4px 8px;
  color: #fff;
  font-family: inherit;
  font-size: 13px;
  outline: none;
  width: 100%;
}

.table-footer-totals {
  padding: 14px 20px;
  background: var(--surface-2);
  border-top: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
  color: var(--muted);
  flex-wrap: wrap;
  gap: 12px;
}

/* Reports KPI Cards */
.reports-kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

@media (max-width: 1100px) {
  .reports-kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.kpi-card {
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.kpi-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.kpi-title {
  font-size: 12px;
  color: var(--muted);
  font-weight: 600;
  text-transform: uppercase;
}

.pill-badge {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.pill-teal {
  background: rgba(45,212,167,0.15);
  color: var(--teal);
}

.pill-coral {
  background: rgba(255,92,108,0.15);
  color: var(--coral);
}

.pill-accent {
  background: rgba(79,91,240,0.15);
  color: var(--accent);
}

.kpi-value {
  font-size: 26px;
  font-weight: 700;
  color: #fff;
  margin: 8px 0;
}

.kpi-sparkline {
  width: 100%;
  height: 38px;
}

/* Chart Grids */
.charts-2col-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 24px;
}

@media (max-width: 1000px) {
  .charts-2col-grid {
    grid-template-columns: 1fr;
  }
}

.chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.chart-title {
  font-size: 16px;
  font-weight: 700;
  color: #fff;
}

.range-pills {
  display: flex;
  background: var(--surface-2);
  border-radius: 8px;
  padding: 2px;
  border: 1px solid var(--border);
}

.range-pill {
  background: transparent;
  border: none;
  color: var(--muted);
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 150ms ease;
}

.range-pill.active {
  background: var(--surface);
  color: #fff;
}

.svg-chart-container {
  width: 100%;
  height: 230px;
  position: relative;
}

.chart-svg {
  width: 100%;
  height: 100%;
  overflow: visible;
}

/* Tooltip floating bubble */
.chart-tooltip {
  position: absolute;
  background: #1a223f;
  border: 1px solid var(--border-focus);
  color: #fff;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 11px;
  pointer-events: none;
  opacity: 0;
  transition: opacity 150ms ease;
  z-index: 50;
  box-shadow: 0 4px 14px rgba(0,0,0,0.5);
  transform: translate(-50%, -120%);
}

/* Settings Sections */
.settings-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
  max-width: 820px;
}

.setting-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 0;
  border-bottom: 1px solid var(--border);
  gap: 16px;
}

.setting-row:last-child {
  border-bottom: none;
}

.setting-info {
  display: flex;
  flex-direction: column;
}

.setting-title {
  font-weight: 600;
  color: #fff;
}

.setting-desc {
  font-size: 12px;
  color: var(--muted);
  margin-top: 2px;
}

.setting-input-num {
  width: 80px;
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 8px 12px;
  color: #fff;
  font-family: inherit;
  font-size: 14px;
  text-align: center;
  outline: none;
}

.setting-input-num:focus {
  border-color: var(--accent);
}

/* Toggles */
.toggle-switch {
  position: relative;
  width: 44px;
  height: 24px;
  display: inline-block;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--surface-2);
  border: 1px solid var(--border);
  transition: .2s;
  border-radius: 24px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 3px;
  bottom: 3px;
  background-color: var(--muted);
  transition: .2s;
  border-radius: 50%;
}

input:checked + .toggle-slider {
  background-color: var(--accent);
  border-color: var(--accent);
}

input:checked + .toggle-slider:before {
  transform: translateX(20px);
  background-color: #fff;
}

/* Modals */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.75);
  backdrop-filter: blur(4px);
  z-index: 1000;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-overlay.show,
.modal-overlay.active {
  display: flex;
}

.modal-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  padding: 28px;
  width: 100%;
  max-width: 540px;
  box-shadow: 0 16px 48px rgba(0,0,0,0.6);
  position: relative;
}

.modal-card-lg {
  max-width: 900px;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.modal-title {
  font-size: 18px;
  font-weight: 700;
  color: #fff;
}

.modal-close-btn {
  background: transparent;
  border: none;
  color: var(--muted);
  cursor: pointer;
  padding: 4px;
}

.modal-close-btn:hover {
  color: #fff;
}

.modal-close-btn svg {
  width: 20px;
  height: 20px;
  stroke: currentColor;
  stroke-width: 2;
}

/* Floating Shortcuts Button */
#btn-open-shortcuts {
  position: fixed;
  bottom: 24px;
  left: 24px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--muted);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  cursor: pointer;
  z-index: 99;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  transition: all 150ms ease;
}

#btn-open-shortcuts:hover {
  color: #fff;
  border-color: var(--accent);
}

/* Away Banner */
#away-banner {
  position: fixed;
  top: 16px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--surface);
  border: 1px solid var(--teal);
  box-shadow: 0 8px 24px rgba(0,0,0,0.5), 0 0 16px rgba(45,212,167,0.25);
  padding: 12px 20px;
  border-radius: 12px;
  display: none;
  align-items: center;
  gap: 12px;
  z-index: 1001;
  color: #fff;
}

#away-banner.show {
  display: flex;
}

/* =========================================
   NEW: Timer Duration Adjuster
   ========================================= */
.timer-duration-adjuster {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 20px;
  padding: 8px 14px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border);
  border-radius: 24px;
  max-width: 480px;
}

.timer-dur-label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  color: var(--muted);
}

.timer-dur-presets {
  display: flex;
  align-items: center;
  gap: 6px;
}

.timer-dur-chip {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border);
  color: var(--text);
  font-size: 12px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 150ms ease;
  user-select: none;
  font-family: inherit;
}

.timer-dur-chip:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  border-color: rgba(255, 255, 255, 0.2);
}

.timer-dur-chip.active {
  background: rgba(79, 91, 240, 0.2);
  border-color: var(--accent);
  color: #fff;
  box-shadow: 0 0 10px rgba(79, 91, 240, 0.3);
}

.timer-dur-custom-wrap {
  display: flex;
  align-items: center;
  gap: 4px;
  background: var(--surface-2);
  padding: 2px 4px 2px 8px;
  border-radius: 12px;
  border: 1px solid var(--border);
}

.timer-custom-dur-input {
  width: 44px;
  background: transparent;
  border: none;
  color: #fff;
  font-size: 12px;
  font-weight: 700;
  font-family: inherit;
  outline: none;
  text-align: center;
}

.timer-custom-dur-input::placeholder {
  color: var(--muted);
  opacity: 0.6;
}

.timer-dur-unit {
  font-size: 11px;
  color: var(--muted);
  margin-right: 2px;
}

/* =========================================
   NEW: Noise Mind Distractions Card
   ========================================= */
.noise-card {
  background: #0E1322;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 18px 20px 20px 20px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
  margin-top: 4px;
}

.noise-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 4px;
}

.noise-title {
  font-size: 14px;
  font-weight: 700;
  color: #FFFFFF;
  letter-spacing: -0.2px;
}

.noise-count {
  font-size: 11px;
  font-weight: 600;
  color: var(--muted);
  background: rgba(255, 255, 255, 0.05);
  padding: 2px 8px;
  border-radius: 10px;
  border: 1px solid var(--border);
}

.noise-desc {
  font-size: 12px;
  color: #64748B;
  margin-bottom: 14px;
  line-height: 1.4;
}

.noise-input-row {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.noise-input {
  flex: 1;
  padding: 8px 12px !important;
  font-size: 13px !important;
  border-radius: 8px !important;
}

.noise-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-height: 240px;
  overflow-y: auto;
}

.noise-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  background: #14192E;
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 8px;
  padding: 8px 12px;
  transition: all 150ms ease;
}

.noise-item:hover {
  background: #181E38;
  border-color: rgba(255, 255, 255, 0.08);
}

.noise-item-text {
  font-size: 13px;
  color: var(--text);
  line-height: 1.35;
  word-break: break-word;
}

.noise-item.cleared .noise-item-text {
  text-decoration: line-through;
  color: var(--muted);
  opacity: 0.6;
}

.noise-empty {
  font-size: 12px;
  color: #64748B;
  padding: 16px 0;
  text-align: center;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px dashed rgba(255, 255, 255, 0.06);
}

/* Rest Group in TimeBlock Toolbar */
.tb-rest-group {
  user-select: none;
}
.btn-tb-rest:hover {
  background: rgba(45, 212, 167, 0.15) !important;
  border-color: var(--teal) !important;
  color: #fff !important;
}

/* ---------- Cloud sync ---------- */
.sync-status {
  margin-top: 10px; width: 100%; display: flex; align-items: center; gap: 8px;
  background: transparent; border: 1px solid var(--border); border-radius: var(--radius-btn);
  padding: 8px 12px; color: var(--muted); font: inherit; font-size: 11px; cursor: pointer; text-align: left;
}
.sync-status:hover { color: var(--text); }
.sync-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--muted); flex: none; }
.sync-status[data-state="idle"] .sync-dot { background: var(--teal); }
.sync-status[data-state="syncing"] .sync-dot { background: var(--accent); animation: syncPulse 1s ease-in-out infinite; }
.sync-status[data-state="offline"] .sync-dot { background: var(--amber); }
.sync-status[data-state="error"] .sync-dot,
.sync-status[data-state="unauthorized"] .sync-dot { background: var(--coral); }
@keyframes syncPulse { 50% { opacity: .35; } }
.sync-settings-status { font-size: 12px; color: var(--muted); padding: 8px 12px; border-radius: var(--radius-btn); background: var(--surface-2); }
.sync-settings-status[data-state="idle"] { color: var(--teal); }
.sync-settings-status[data-state="error"],
.sync-settings-status[data-state="unauthorized"] { color: var(--coral); }
.sync-settings-status[data-state="offline"] { color: var(--amber); }
.sync-input { flex: 1; min-width: 220px; padding: 9px 12px; font-size: 13px; }

/* ---------- Installable app ---------- */
.install-app-btn {
  margin-top: 8px; width: 100%; display: flex; align-items: center; justify-content: center; gap: 8px;
  background: var(--accent); border: 0; border-radius: var(--radius-btn); padding: 8px 12px;
  color: #fff; font: inherit; font-size: 12px; font-weight: 600; cursor: pointer;
}
.install-app-btn:hover { filter: brightness(1.1); }
#update-bar {
  position: fixed; left: 50%; bottom: 20px; transform: translateX(-50%); z-index: 99998;
  display: none; align-items: center; gap: 14px; padding: 10px 12px 10px 18px;
  background: var(--surface); border: 1px solid var(--border-focus); border-radius: 999px;
  color: var(--text); font-size: 13px; box-shadow: 0 8px 30px rgba(0,0,0,.45); max-width: calc(100vw - 32px);
}
#update-bar button {
  background: var(--accent); color: #fff; border: 0; border-radius: 999px; padding: 6px 14px;
  font: inherit; font-weight: 700; cursor: pointer; white-space: nowrap;
}


/* ---------- Review ---------- */
.rv-nav { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 18px; }
.rv-arrow { min-width: 36px; justify-content: center; font-size: 18px; line-height: 1; }
.rv-nav-label { font-size: 15px; font-weight: 700; color: #fff; margin-left: 6px; }
.rv-weekstart { margin-left: auto; font-size: 12px; color: var(--muted); display: flex; align-items: center; gap: 8px; }
.rv-kpis { margin-bottom: 20px; }
.rv-kpi-sub { font-size: 12px; color: var(--muted); }
.rv-kpi-small { font-size: 20px; }
.rv-good { color: var(--teal) !important; }
.rv-mid { color: var(--amber) !important; }
.rv-bad { color: var(--coral) !important; }
.rv-grid { display: grid; grid-template-columns: minmax(0, 1fr) 360px; gap: 20px; align-items: start; }
.rv-side { display: flex; flex-direction: column; gap: 20px; }
@media (max-width: 1100px) { .rv-grid { grid-template-columns: 1fr; } }
.rv-table-card { padding: 20px 20px 16px; overflow-x: auto; }
.rv-table { width: 100%; }
.rv-table th:first-child, .rv-table td:first-child { padding-left: 4px; }
.rv-table td { vertical-align: middle; }
.rv-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 8px; flex-shrink: 0; }
.rv-over { color: var(--amber); }
.rv-under { color: var(--muted); }
.rv-pill { font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 10px; white-space: nowrap; }
.rv-pill-done { background: rgba(45,212,167,0.15); color: var(--teal); }
.rv-pill-part { background: rgba(255,182,72,0.15); color: var(--amber); }
.rv-pill-open { background: rgba(255,255,255,0.06); color: var(--muted); }
.rv-pill-moved { background: rgba(124,92,255,0.15); color: var(--accent-2); }
.rv-carried { font-size: 11px; color: var(--accent-2); margin-left: 6px; }
.rv-empty { font-size: 13px; color: var(--muted); padding: 6px 0; }
.rv-footnote { font-size: 11px; color: var(--muted); margin-top: 12px; }
.rv-carry-row { display: flex; align-items: center; gap: 8px; padding: 8px 0; border-bottom: 1px solid var(--border); font-size: 13px; cursor: pointer; }
.rv-carry-row:last-child { border-bottom: 0; }
.rv-carry-label { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: var(--text); }
.rv-carry-left { color: var(--muted); font-size: 12px; white-space: nowrap; }
.rv-textarea { resize: vertical; min-height: 90px; font-size: 14px; line-height: 1.5; }
.rv-shutdown { display: flex; align-items: center; gap: 10px; margin-top: 12px; font-size: 14px; color: var(--text); cursor: pointer; }
.rv-shutdown input { width: 18px; height: 18px; accent-color: var(--teal); }
.rv-save-status { font-size: 11px; color: var(--muted); }
.rv-nowrap { white-space: nowrap; }
.rv-check { color: var(--teal); font-weight: 700; }
.rv-day-row { cursor: pointer; }
.rv-day-row:hover td { background: rgba(255,255,255,0.02); }
.rv-bar-cell { width: 34%; min-width: 120px; }
.rv-bar-track { position: relative; height: 14px; }
.rv-bar-plan, .rv-bar-focus { position: absolute; left: 0; border-radius: 4px; }
.rv-bar-plan { top: 0; height: 14px; background: rgba(255,255,255,0.08); }
.rv-bar-focus { top: 4px; height: 6px; background: linear-gradient(90deg, var(--accent), var(--accent-2)); }
.rv-legend { font-size: 11px; color: var(--muted); display: flex; align-items: center; gap: 6px; }
.rv-leg-plan, .rv-leg-focus { display: inline-block; width: 12px; height: 8px; border-radius: 3px; margin-left: 8px; }
.rv-leg-plan { background: rgba(255,255,255,0.15); }
.rv-leg-focus { background: var(--accent); }
.rv-hbar { display: grid; grid-template-columns: minmax(90px, 160px) 1fr auto; align-items: center; gap: 10px; padding: 6px 0; font-size: 13px; }
.rv-hbar-name { display: flex; align-items: center; min-width: 0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; color: var(--text); }
.rv-hbar-track { height: 8px; background: rgba(255,255,255,0.05); border-radius: 4px; overflow: hidden; }
.rv-hbar-fill { display: block; height: 100%; border-radius: 4px; }
.rv-hbar-val { color: var(--muted); font-size: 12px; white-space: nowrap; }
.rv-notes-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.rv-label { font-size: 12px; color: var(--muted); margin-bottom: 6px; font-weight: 600; }
#review-bar {
  position: fixed; left: 50%; bottom: 20px; transform: translateX(-50%); z-index: 99997;
  display: none; align-items: center; gap: 10px; padding: 10px 12px 10px 18px;
  background: var(--surface); border: 1px solid rgba(45,212,167,0.45); border-radius: 999px;
  color: var(--text); font-size: 13px; box-shadow: 0 8px 30px rgba(0,0,0,.45); max-width: calc(100vw - 32px);
}
#review-bar button { background: var(--teal); color: #06231b; border: 0; border-radius: 999px; padding: 6px 14px; font: inherit; font-weight: 700; cursor: pointer; white-space: nowrap; }
#review-bar button.rv-later { background: transparent; color: var(--muted); padding: 6px 8px; }

/* =========================================
   PHONE LAYOUT (narrow screens only; desktop is unchanged)
   ========================================= */
@media (max-width: 760px) {
  #app-container { display: block; }

  /* Sidebar becomes a bottom tab bar */
  #sidebar {
    position: fixed; top: auto; bottom: 0; left: 0; right: 0;
    width: 100%; height: auto; flex-direction: row; align-items: stretch;
    padding: 4px 2px calc(4px + env(safe-area-inset-bottom));
    border-right: 0; border-top: 1px solid var(--border);
    background-color: rgb(12,17,32);
    z-index: 500;
  }
  #sidebar .brand-logo, #sidebar .streak-card, #btn-install-app { display: none !important; }
  .nav-menu { flex-direction: row; gap: 0; flex: 1; justify-content: space-around; }
  .nav-item {
    flex: 1 1 0; min-width: 0; flex-direction: column; justify-content: center; gap: 3px;
    padding: 6px 2px; margin: 0; font-size: 10px; text-align: center;
  }
  .nav-item svg { width: 20px; height: 20px; flex-shrink: 0; }
  .nav-item span { display: block; max-width: 100%; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .nav-item[data-short] span { display: none; }
  .nav-item[data-short]::after { content: attr(data-short); display: block; white-space: nowrap; }

  /* Log filters wrap; search takes the full row */
  .log-filter-row { flex-wrap: wrap; min-width: 0 !important; }
  #log-search-input { max-width: none !important; flex: 1 1 100%; }

  /* Sync status: small pill at the top right */
  .sidebar-bottom {
    position: fixed; top: calc(8px + env(safe-area-inset-top)); right: 12px;
    padding: 0; border: 0; margin: 0; z-index: 501;
  }
  .sync-status {
    width: auto; margin: 0; padding: 4px 10px; font-size: 10px;
    background: var(--surface); border-radius: 999px;
  }

  /* Content: full width, room for the top pill and the bottom bar */
  #main-content { height: auto; min-height: 100vh; overflow: visible; }
  .view-container { padding: calc(44px + env(safe-area-inset-top)) 16px calc(86px + env(safe-area-inset-bottom)); }
  .view-header { margin-bottom: 16px; }
  .view-title { font-size: 20px; }
  .card { padding: 16px; border-radius: 16px; }

  /* Grids collapse to one column */
  .timer-view-grid, .charts-2col-grid, .settings-grid, .skills-grid { grid-template-columns: 1fr !important; }
  .reports-kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)) !important; gap: 12px; }
  .tb-container { flex-direction: column; }
  .tb-builder-panel, .tb-timeline-panel { width: 100%; }

  /* Timer: smaller dial, Start/Pause right under the task, duration options after */
  .timer-card { padding: 18px 16px 20px; }
  .mode-badge { margin-bottom: 12px; }
  .timer-dial-wrap { width: 210px; height: 210px; margin-bottom: 12px; }
  .timer-digits { font-size: 50px; }
  .wave-band-container { display: none; }
  .task-binder-row { order: 1; }
  .timer-controls { order: 2; margin-top: 14px; }
  .timer-duration-adjuster { order: 3; margin-top: 16px; }
  .timer-card > div[style*="margin-top: 14px"] { order: 4; }
  .stats-grid-row { order: 5; }

  /* Tables scroll sideways inside their card instead of stretching the page */
  .table-card { overflow-x: auto; -webkit-overflow-scrolling: touch; }

  /* Dialogs fit the screen */
  .modal-card, .modal-card-lg {
    width: calc(100vw - 24px) !important; max-width: none !important;
    max-height: calc(100vh - 32px); overflow-y: auto; padding: 18px;
  }

  #update-bar, #review-bar { bottom: calc(76px + env(safe-area-inset-bottom)); }
  #review-bar { flex-wrap: wrap; justify-content: center; border-radius: 16px; text-align: center; }
  .rv-tabs { width: 100%; }
  .rv-tabs .rv-tab { flex: 1; }
  .rv-weekstart { margin-left: 0; width: 100%; }
  .rv-notes-grid { grid-template-columns: 1fr; }
  .rv-bar-cell, .rv-bar-head { display: none; }
  .rv-hbar { grid-template-columns: minmax(80px, 120px) 1fr auto; }
  #toast-container { bottom: calc(80px + env(safe-area-inset-bottom)) !important; }
}
"""
