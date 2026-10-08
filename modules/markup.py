# HTML Markup module for FocusDeck
BODY_MARKUP = """
<div id="app-container">
  <!-- =========================================
       SIDEBAR
       ========================================= -->
  <aside id="sidebar">
    <div class="brand-logo">
      <div class="brand-icon">
        <svg viewBox="0 0 24 24" width="20" height="20" stroke="#fff" stroke-width="2.2" fill="none">
          <circle cx="12" cy="12" r="10" />
          <polyline points="12 6 12 12 16 14" />
        </svg>
      </div>
      <div class="brand-name">FocusDeck</div>
    </div>

    <nav class="nav-menu">
      <button class="nav-item active" data-view="timer" id="nav-timer">
        <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        <span>Timer</span>
      </button>
      <button class="nav-item" data-view="timeblock" id="nav-timeblock">
        <svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><line x1="10" y1="14" x2="14" y2="14"/></svg>
        <span>Time Block</span>
      </button>
      <button class="nav-item" data-view="log" id="nav-log">
        <svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
        <span>Log</span>
      </button>
      <button class="nav-item" data-view="reports" id="nav-reports">
        <svg viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
        <span>Reports</span>
      </button>
      <button class="nav-item" data-view="skills" id="nav-skills" data-short="Hours">
        <svg viewBox="0 0 24 24"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.45 1-1 1H7.5a1.5 1.5 0 0 0 0 3h9a1.5 1.5 0 0 0 0-3H15c-.55 0-1-.45-1-1v-2.34"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2z"/></svg>
        <span>10,000 Hours</span>
      </button>
      <button class="nav-item" data-view="settings" id="nav-settings">
        <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
        <span>Settings</span>
      </button>
    </nav>

    <div class="sidebar-bottom">
      <div class="streak-card">
        <div class="streak-info">
          <span class="streak-label">Daily Streak</span>
          <div class="streak-val">
            <svg viewBox="0 0 24 24" width="16" height="16" stroke="var(--amber)" stroke-width="2.2" fill="none"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/></svg>
            <span id="sb-streak-count">0d</span>
          </div>
        </div>
        <div class="daily-goal-prog">
          <span style="font-size:11px; color:var(--muted);" id="sb-goal-text">0m / 240m</span>
          <div class="prog-bar-bg" style="width:60px;">
            <div class="prog-bar-fill" id="sb-goal-fill"></div>
          </div>
        </div>
      </div>
      <button type="button" class="sync-status" id="sync-status" data-state="off" title="Cloud sync">
        <span class="sync-dot"></span>
        <span id="sync-status-text">Sync off</span>
      </button>
      <button type="button" class="install-app-btn" id="btn-install-app" style="display:none;">
        <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2.2" fill="none"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
        <span>Install app</span>
      </button>
    </div>
  </aside>

  <!-- =========================================
       MAIN CONTENT CONTAINER
       ========================================= -->
  <main id="main-content">
    <!-- VIEW 1: TIMER -->
    <section class="view-container active" id="view-timer">
      <div class="timer-view-grid">
        <!-- Main Hero Timer -->
        <div class="card timer-card" id="timer-card">
          <div class="mode-badge" id="timer-mode-badge">FOCUS</div>

          <div class="timer-dial-wrap">
            <svg class="timer-svg" viewBox="0 0 260 260">
              <defs>
                <linearGradient id="timerGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#4F5BF0" />
                  <stop offset="100%" stop-color="#7C5CFF" />
                </linearGradient>
              </defs>
              <circle class="timer-ring-bg" cx="130" cy="130" r="118" />
              <circle class="timer-ring-circle" id="timer-ring-circle" cx="130" cy="130" r="118" />
            </svg>
            <div class="timer-center-content">
              <div class="timer-digits" id="timer-digits">25:00</div>
              <div class="timer-cycle-dots" id="timer-cycle-dots"></div>
            </div>
          </div>

          <!-- The Wave Band -->
          <div class="wave-band-container wave-idle" id="wave-container">
            <svg viewBox="0 0 1200 60" preserveAspectRatio="none">
              <defs>
                <linearGradient id="waveGrad1" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stop-color="#4F5BF0" stop-opacity="0.8"/>
                  <stop offset="50%" stop-color="#7C5CFF" stop-opacity="0.6"/>
                  <stop offset="100%" stop-color="#4F5BF0" stop-opacity="0.8"/>
                </linearGradient>
                <linearGradient id="waveGrad2" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stop-color="#2DD4A7" stop-opacity="0.6"/>
                  <stop offset="50%" stop-color="#4F5BF0" stop-opacity="0.5"/>
                  <stop offset="100%" stop-color="#2DD4A7" stop-opacity="0.6"/>
                </linearGradient>
                <linearGradient id="waveGrad3" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stop-color="#FF4FA3" stop-opacity="0.4"/>
                  <stop offset="50%" stop-color="#7C5CFF" stop-opacity="0.4"/>
                  <stop offset="100%" stop-color="#FF4FA3" stop-opacity="0.4"/>
                </linearGradient>
              </defs>
              <path class="wave-path wave-1" fill="url(#waveGrad1)" d="M 0 30 Q 150 10 300 30 T 600 30 T 900 30 T 1200 30 L 1200 60 L 0 60 Z" />
              <path class="wave-path wave-2" fill="url(#waveGrad2)" d="M 0 32 Q 200 15 400 32 T 800 32 T 1200 32 L 1200 60 L 0 60 Z" />
              <path class="wave-path wave-3" fill="url(#waveGrad3)" d="M 0 35 Q 100 20 200 35 T 400 35 T 600 35 T 800 35 T 1000 35 T 1200 35 L 1200 60 L 0 60 Z" />
            </svg>
          </div>

          <!-- Task & Tag Binder -->
          <div class="task-binder-row">
            <div class="task-input-wrapper">
              <input type="text" class="task-input" id="task-label-input" placeholder="What are you working on?" list="recent-labels-datalist" autocomplete="off" />
              <datalist id="recent-labels-datalist"></datalist>
            </div>
            <div class="tags-chips" id="tags-chips-container"></div>
          </div>

          <!-- Quick Duration Presets / Custom Duration -->
          <div class="timer-duration-adjuster" id="timer-duration-adjuster">
            <span class="timer-dur-label">Duration:</span>
            <div class="timer-dur-presets">
              <button type="button" class="timer-dur-chip" data-min="15">15m</button>
              <button type="button" class="timer-dur-chip active" data-min="25">25m</button>
              <button type="button" class="timer-dur-chip" data-min="37">37m</button>
              <button type="button" class="timer-dur-chip" data-min="45">45m</button>
              <button type="button" class="timer-dur-chip" data-min="60">60m</button>
            </div>
            <div class="timer-dur-custom-wrap">
              <input type="number" id="timer-custom-dur-input" class="timer-custom-dur-input" min="1" max="720" placeholder="37" title="Enter custom minutes" />
              <span class="timer-dur-unit">m</span>
              <button type="button" class="btn btn-secondary btn-sm" id="btn-set-custom-dur" style="padding:4px 8px; font-size:11px;">Set</button>
            </div>
          </div>

          <!-- Controls -->
          <div class="timer-controls">
            <button class="btn btn-secondary btn-sm" id="btn-timer-reset" title="Reset (R)">
              <svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
              <span>Reset</span>
            </button>
            <button class="btn btn-primary btn-pulse-idle" id="btn-timer-primary">
              <svg id="primary-btn-icon" viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3" fill="currentColor"/></svg>
              <span id="primary-btn-label">Start Focus</span>
            </button>
            <button class="btn btn-secondary btn-sm" id="btn-timer-skip" title="Skip to next (S)">
              <svg viewBox="0 0 24 24"><polygon points="5 4 15 12 5 20 5 4"/><line x1="19" y1="5" x2="19" y2="19"/></svg>
              <span>Skip</span>
            </button>
          </div>

          <div style="margin-top: 14px;">
            <button class="btn btn-danger btn-sm" id="btn-timer-early" style="display:none;">End & Save Early</button>
          </div>
        </div>

        <!-- Right Column Panels -->
        <div class="right-column-stack">
          <!-- 3 Mini Stats -->
          <div class="stats-grid-row">
            <div class="stat-card stat-card-focus">
              <div class="stat-card-label">FOCUS TODAY</div>
              <div class="stat-card-value" id="stat-today-focus">0m</div>
              <svg class="stat-card-corner" viewBox="0 0 60 36" preserveAspectRatio="none">
                <path d="M 0 35 L 28 35 L 59 4 L 59 35 Z" fill="rgba(79, 91, 240, 0.08)" />
                <path d="M 0 35 L 28 35 L 59 4" fill="none" stroke="#4F5BF0" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
            </div>
            <div class="stat-card stat-card-sessions">
              <div class="stat-card-label">SESSIONS</div>
              <div class="stat-card-value" id="stat-today-sessions">0</div>
              <svg class="stat-card-corner" viewBox="0 0 60 36" preserveAspectRatio="none">
                <path d="M 0 35 L 28 35 L 59 4 L 59 35 Z" fill="rgba(45, 212, 167, 0.08)" />
                <path d="M 0 35 L 28 35 L 59 4" fill="none" stroke="#2DD4A7" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
            </div>
            <div class="stat-card stat-card-paused">
              <div class="stat-card-label">PAUSED</div>
              <div class="stat-card-value stat-card-val-coral" id="stat-today-interruptions">0</div>
              <svg class="stat-card-corner" viewBox="0 0 60 36" preserveAspectRatio="none">
                <path d="M 0 35 L 28 35 L 59 4 L 59 35 Z" fill="rgba(255, 92, 108, 0.08)" />
                <path d="M 0 35 L 28 35 L 59 4" fill="none" stroke="#FF5C6C" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
            </div>
          </div>

          <!-- Recent Sessions Card -->
          <div class="card recent-sessions-card">
            <div class="recent-sessions-header">
              <div>
                <div class="recent-sessions-title">Recent Sessions</div>
                <div class="recent-sessions-subtitle">Last 6 completed sessions</div>
              </div>
              <button class="recent-sessions-view-all" id="link-view-all-log">View All</button>
            </div>
            <div class="recent-sessions-list" id="recent-sessions-list"></div>
          </div>

          <!-- Noise & Distraction Parked Thoughts Card (Below Recent Sessions) -->
          <div class="card noise-card" id="noise-card">
            <div class="noise-header">
              <div style="display:flex; align-items:center; gap:8px;">
                <svg viewBox="0 0 24 24" width="16" height="16" stroke="var(--amber)" stroke-width="2" fill="none">
                  <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
                </svg>
                <div class="noise-title">Session Mind Noise & Distractions</div>
              </div>
              <span class="noise-count" id="noise-count-badge">0 items</span>
            </div>
            <div class="noise-desc">Jot down intrusive thoughts, sudden chores, or mental noises without breaking your focus.</div>

            <div class="noise-input-row">
              <input type="text" class="task-input noise-input" id="noise-thought-input" placeholder="Write a noise or thought... (Press Enter)" autocomplete="off" />
              <button class="btn btn-secondary btn-sm" id="btn-add-noise" style="padding:8px 12px; font-size:12px;">Add</button>
            </div>

            <div class="noise-list" id="noise-items-list"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- VIEW 2: TIME BLOCK (NEW) -->
    <section class="view-container" id="view-timeblock">
      <div class="view-header">
        <div>
          <div class="view-title">Time Block Planner</div>
          <div class="view-desc">Cal Newport whole-day intentional time-blocking with real-time tracking</div>
        </div>

        <!-- Date & Day Window Navigator -->
        <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
          <div class="tb-date-nav">
            <button class="icon-btn-sm" id="tb-btn-prev-day" title="Previous Day">
              <svg viewBox="0 0 24 24"><polyline points="15 18 9 12 15 6"/></svg>
            </button>
            <button class="btn btn-secondary btn-sm" id="tb-btn-today" style="padding:4px 10px;">Today</button>
            <button class="icon-btn-sm" id="tb-btn-next-day" title="Next Day">
              <svg viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
            <input type="date" id="tb-date-picker" style="background:transparent; border:none; color:#fff; font-family:inherit; font-size:13px; font-weight:600; cursor:pointer; padding:2px 6px;" />
            <span id="tb-date-weekday" class="tb-date-weekday"></span>
          </div>

          <div class="tb-daywindow-controls">
            <span>Day runs from</span>
            <input type="time" class="tb-time-input" id="tb-window-start" value="08:00" />
            <span>to</span>
            <input type="time" class="tb-time-input" id="tb-window-end" value="22:00" />
          </div>
        </div>
      </div>

      <div class="tb-container">
        <!-- Left Panel: Block Builder -->
        <div class="tb-builder-panel">
          <div class="card" style="padding:18px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
              <span style="font-weight:700; color:#fff; font-size:14px;">Day Plan Blocks</span>
              <span style="font-size:12px; color:var(--muted);" id="tb-builder-stats">0 blocks • 0m</span>
            </div>

            <div class="tb-blocks-list" id="tb-blocks-list"></div>

            <div style="margin-top:14px; border-top:1px solid var(--border); padding-top:14px;">
              <button class="btn btn-primary" id="btn-tb-open-add" style="width:100%; font-size:13px; padding:10px;">
                <svg viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                <span>Add Block</span>
              </button>
            </div>
          </div>

          <!-- Sticky Note / Freeform Scratchpad -->
          <div class="card tb-sticky-note-card">
            <div class="tb-sticky-note-tape"></div>
            <div class="tb-sticky-note-header">
              <div style="display:flex; align-items:center; gap:6px;">
                <span style="font-size:14px;">📌</span>
                <span class="tb-sticky-note-title">Planning Sticky Note</span>
              </div>
              <div style="display:flex; align-items:center; gap:8px;">
                <span class="tb-sticky-save-status" id="tb-sticky-save-status">Auto-saved</span>
                <button type="button" class="icon-btn-sm" id="btn-tb-sticky-clear" title="Clear notes" style="padding:2px 4px; color:var(--muted); opacity:0.75;">
                  <svg viewBox="0 0 24 24" width="13" height="13" stroke="currentColor" fill="none"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                </button>
              </div>
            </div>

            <div class="tb-sticky-note-sub">Freeform scratchpad for rough plans & thoughts (not in blocks)</div>

            <textarea 
              id="tb-sticky-note-input" 
              class="tb-sticky-note-textarea" 
              placeholder="Type freely here... Write down today's rough plan, thoughts, or reminders without adding them into scheduled blocks."
              rows="5"
            ></textarea>

            <div class="tb-sticky-note-footer">
              <span id="tb-sticky-note-meta" style="font-size:11px; color:rgba(253,230,138,0.5);">0 words</span>
              <button type="button" class="btn btn-secondary btn-sm" id="btn-tb-note-to-block" style="padding:3px 9px; font-size:11px; border-color:rgba(245,158,11,0.3); color:#FBBF24;" title="Convert selected text or rough plan into a schedule block">
                + Add as Block
              </button>
            </div>
          </div>
        </div>

        <!-- Main Panel: Timeline Canvas -->
        <div class="tb-timeline-panel">
          <div class="card tb-timeline-card">
            <!-- Timeline Toolbar -->
            <div class="tb-toolbar">
              <!-- Far Left: Rest buttons & Reschedule -->
              <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                <div class="tb-rest-group" style="display:flex; align-items:center; gap:4px;">
                  <span style="font-size:11px; font-weight:600; color:var(--teal); margin-right:2px; display:inline-flex; align-items:center; gap:3px;">
                    <svg viewBox="0 0 24 24" width="13" height="13" stroke="currentColor" stroke-width="2" fill="none"><path d="M18 8h1a4 4 0 0 1 0 8h-1"/><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"/><line x1="6" y1="1" x2="6" y2="4"/><line x1="10" y1="1" x2="10" y2="4"/><line x1="14" y1="1" x2="14" y2="4"/></svg>
                    Rest:
                  </span>
                  <button type="button" class="btn btn-secondary btn-sm btn-tb-rest" data-min="5" title="Add 5-min Rest Block" style="padding:4px 8px; font-size:11px; border-color:rgba(45,212,167,0.3); color:var(--teal);">+5m</button>
                  <button type="button" class="btn btn-secondary btn-sm btn-tb-rest" data-min="15" title="Add 15-min Rest Block" style="padding:4px 8px; font-size:11px; border-color:rgba(45,212,167,0.3); color:var(--teal);">+15m</button>
                  <button type="button" class="btn btn-secondary btn-sm btn-tb-rest" data-min="30" title="Add 30-min Rest Block" style="padding:4px 8px; font-size:11px; border-color:rgba(45,212,167,0.3); color:var(--teal);">+30m</button>
                </div>

                <button class="btn btn-secondary btn-sm" id="btn-tb-reschedule" style="display:none;" title="Shift subsequent blocks later by overrun">
                  <svg viewBox="0 0 24 24" style="color:var(--coral);"><path d="M12 8v4l3 3"/><circle cx="12" cy="12" r="9"/></svg>
                  <span>Reschedule Remaining Day</span>
                  <span class="pill-badge pill-coral" id="tb-reschedule-amount">+0m</span>
                </button>
              </div>

              <!-- Far Right: Plan Actions -->
              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                <button class="btn btn-secondary btn-sm" id="btn-tb-copy-yesterday" title="Copy blocks from yesterday">Copy Yesterday</button>
                <button class="btn btn-secondary btn-sm" id="btn-tb-load-template" title="Load recurring template">Load Template</button>
                <button class="btn btn-secondary btn-sm" id="btn-tb-save-template" title="Save current day as template">Save as Template</button>
              </div>
            </div>

            <!-- Scrollable Timeline Track -->
            <div class="tb-timeline-scroll" id="tb-timeline-scroll">
              <div class="tb-hour-labels" id="tb-hour-labels"></div>
              <div class="tb-track" id="tb-track"></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- VIEW 3: LOG -->
    <section class="view-container" id="view-log">
      <div class="view-header">
        <div>
          <div class="view-title">Session History Log</div>
          <div class="view-desc">Complete record of your focused sessions and mindful breaks</div>
        </div>
        <div style="display:flex; gap:10px;">
          <button class="btn btn-primary btn-sm" id="btn-add-manual">
            <svg viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
            <span>+ Manual Entry</span>
          </button>
        </div>
      </div>

      <div class="card table-card">
        <div class="log-toolbar">
          <div class="log-filter-row" style="display:flex; gap:12px; align-items:center; flex:1; min-width:260px;">
            <input type="text" class="task-input" id="log-search-input" placeholder="Search sessions, labels, tags, notes..." style="padding:8px 12px; font-size:13px; max-width:320px;" />
            <select class="tb-time-input" id="log-date-filter" style="padding:8px 12px;">
              <option value="all">All Time</option>
              <option value="today">Today</option>
              <option value="7d">Last 7 Days</option>
              <option value="30d">Last 30 Days</option>
              <option value="custom">Custom Range</option>
            </select>
            <div id="log-custom-dates" style="display:none; gap:6px; align-items:center;">
              <input type="date" class="tb-time-input" id="log-custom-start" />
              <span>to</span>
              <input type="date" class="tb-time-input" id="log-custom-end" />
            </div>
            <select class="tb-time-input" id="log-mode-filter" style="padding:8px 12px;">
              <option value="all">All Modes</option>
              <option value="focus">Focus Only</option>
              <option value="breaks">Breaks Only</option>
            </select>
          </div>

          <div style="display:flex; gap:8px;">
            <button class="btn btn-secondary btn-sm" id="btn-export-csv" title="Download CSV">Export CSV</button>
            <button class="btn btn-secondary btn-sm" id="btn-export-json" title="Export sessions JSON">Export JSON</button>
            <label class="btn btn-secondary btn-sm" style="cursor:pointer; margin:0;" title="Import sessions JSON">
              <span>Import JSON</span>
              <input type="file" id="import-json-file" accept=".json" style="display:none;" />
            </label>
          </div>
        </div>

        <div class="table-responsive">
          <table class="data-table" id="log-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Time</th>
                <th>Mode</th>
                <th>Task Label</th>
                <th>Tags</th>
                <th>Planned</th>
                <th>Actual</th>
                <th style="text-align:center;">Done</th>
                <th style="text-align:center;">Pauses</th>
                <th>Note</th>
                <th style="text-align:right;">Actions</th>
              </tr>
            </thead>
            <tbody id="log-table-body"></tbody>
          </table>
        </div>

        <div class="table-footer-totals">
          <div>Showing <strong id="log-filtered-count">0</strong> sessions</div>
          <div style="display:flex; gap:20px;">
            <span>Total Focus Time: <strong id="log-filtered-total-time">0h 0m</strong></span>
            <span>Average Session: <strong id="log-filtered-avg-time">0m</strong></span>
          </div>
        </div>
      </div>
    </section>

    <!-- VIEW 4: REPORTS -->
    <section class="view-container" id="view-reports">
      <div class="view-header">
        <div>
          <div class="view-title">Productivity Analytics</div>
          <div class="view-desc">Deep-dive visual reporting hand-crafted from your focus patterns</div>
        </div>
      </div>

      <!-- 4 Top KPI Cards -->
      <div class="reports-kpi-grid">
        <div class="card kpi-card">
          <div class="kpi-header">
            <span class="kpi-title">Total Focus Time</span>
            <span class="pill-badge pill-teal" id="rep-badge-time">+0%</span>
          </div>
          <div class="kpi-value" id="rep-val-time">0h</div>
          <svg class="kpi-sparkline" id="rep-spark-time" preserveAspectRatio="none" viewBox="0 0 100 38"></svg>
        </div>

        <div class="card kpi-card">
          <div class="kpi-header">
            <span class="kpi-title">Sessions Completed</span>
            <span class="pill-badge pill-teal" id="rep-badge-sessions">+0%</span>
          </div>
          <div class="kpi-value" id="rep-val-sessions">0</div>
          <svg class="kpi-sparkline" id="rep-spark-sessions" preserveAspectRatio="none" viewBox="0 0 100 38"></svg>
        </div>

        <div class="card kpi-card">
          <div class="kpi-header">
            <span class="kpi-title">Avg Session Length</span>
            <span class="pill-badge pill-teal" id="rep-badge-avg">+0%</span>
          </div>
          <div class="kpi-value" id="rep-val-avg">0m</div>
          <svg class="kpi-sparkline" id="rep-spark-avg" preserveAspectRatio="none" viewBox="0 0 100 38"></svg>
        </div>

        <div class="card kpi-card">
          <div class="kpi-header">
            <span class="kpi-title">Completion Rate</span>
            <span class="pill-badge pill-teal" id="rep-badge-rate">+0%</span>
          </div>
          <div class="kpi-value" id="rep-val-rate">0%</div>
          <svg class="kpi-sparkline" id="rep-spark-rate" preserveAspectRatio="none" viewBox="0 0 100 38"></svg>
        </div>
      </div>

      <!-- Charts 2-Column Grid -->
      <div class="charts-2col-grid">
        <!-- Focus vs Goal Bar Chart -->
        <div class="card" style="padding:20px;">
          <div class="chart-header">
            <div class="chart-title">Focus vs Daily Goal (Last 10 Days)</div>
            <div style="font-size:11px; color:var(--muted); display:flex; gap:12px;">
              <span style="display:flex; align-items:center; gap:4px;"><span style="width:8px; height:8px; background:var(--accent); border-radius:2px;"></span> Goal Base</span>
              <span style="display:flex; align-items:center; gap:4px;"><span style="width:8px; height:8px; background:var(--teal); border-radius:2px;"></span> Surplus</span>
            </div>
          </div>
          <div class="svg-chart-container">
            <svg class="chart-svg" id="svg-chart-goal" viewBox="0 0 500 230"></svg>
            <div class="chart-tooltip" id="tooltip-goal"></div>
          </div>
        </div>

        <!-- Focus Trend Area Chart -->
        <div class="card" style="padding:20px;">
          <div class="chart-header">
            <div class="chart-title">Focus Trend</div>
            <div class="range-pills" id="trend-range-pills">
              <button class="range-pill active" data-range="day">Day</button>
              <button class="range-pill" data-range="week">Week</button>
              <button class="range-pill" data-range="month">Month</button>
              <button class="range-pill" data-range="year">Year</button>
            </div>
          </div>
          <div class="svg-chart-container">
            <svg class="chart-svg" id="svg-chart-trend" viewBox="0 0 500 230"></svg>
            <div class="chart-tooltip" id="tooltip-trend"></div>
          </div>
        </div>
      </div>

      <!-- Bottom Charts: Donut & Heatmap & Streak -->
      <div class="charts-2col-grid">
        <!-- Time by Label Donut -->
        <div class="card" style="padding:20px;">
          <div class="chart-header">
            <div class="chart-title">Time by Task Label</div>
          </div>
          <div style="display:flex; align-items:center; gap:24px; min-height:200px;">
            <div style="position:relative; width:160px; height:160px; flex-shrink:0;">
              <svg viewBox="0 0 200 200" id="svg-chart-donut" style="width:100%; height:100%;"></svg>
              <div style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); text-align:center;">
                <div style="font-size:18px; font-weight:800; color:#fff;" id="donut-center-hours">0h</div>
                <div style="font-size:10px; color:var(--muted); text-transform:uppercase;">Total</div>
              </div>
            </div>
            <div style="flex:1; display:flex; flex-direction:column; gap:8px;" id="donut-legend-container"></div>
          </div>
        </div>

        <!-- Time of Day Heatmap & Streak -->
        <div class="card" style="padding:20px; display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div class="chart-header">
              <div class="chart-title">Time of Day Focus Heatmap</div>
              <span style="font-size:11px; color:var(--muted);">00:00 - 23:00</span>
            </div>
            <div style="position:relative; width:100%; height:110px;">
              <svg viewBox="0 0 500 110" id="svg-chart-heatmap" style="width:100%; height:100%;"></svg>
              <div class="chart-tooltip" id="tooltip-heatmap"></div>
            </div>
          </div>

          <div style="border-top:1px solid var(--border); padding-top:14px; margin-top:12px; display:flex; justify-content:space-between; align-items:center;">
            <div>
              <div style="font-size:11px; color:var(--muted); text-transform:uppercase;">Streak Consistency (12 Weeks)</div>
              <div style="display:flex; gap:14px; margin-top:4px;">
                <span>Current: <strong style="color:var(--amber);" id="rep-current-streak">0 days</strong></span>
                <span>Longest: <strong style="color:#fff;" id="rep-longest-streak">0 days</strong></span>
              </div>
            </div>
            <div style="position:relative; height:56px;">
              <svg viewBox="0 0 100 56" id="svg-chart-contribution" style="height:100%;"></svg>
              <div class="chart-tooltip" id="tooltip-contribution"></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- VIEW 5: 10,000 HOURS (NEW) -->
    <section class="view-container" id="view-skills">
      <div class="view-header">
        <div>
          <div class="view-title">10,000 Hours Mastery Tracker</div>
          <div class="view-desc">Deliberate practice progress aggregated automatically from your focus sessions</div>
        </div>
        <button class="btn btn-primary" id="btn-open-add-skill">
          <svg viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          <span>Add Skill</span>
        </button>
      </div>

      <!-- Skills Cards Grid -->
      <div class="skills-grid" id="skills-grid"></div>

      <!-- Empty State -->
      <div class="card" id="skills-empty-state" style="display:none; text-align:center; padding:50px 24px;">
        <div style="width:64px; height:64px; border-radius:50%; background:rgba(255,182,72,0.1); border:1px solid rgba(255,182,72,0.3); display:flex; align-items:center; justify-content:center; margin:0 auto 18px auto;">
          <svg viewBox="0 0 24 24" width="32" height="32" stroke="var(--amber)" stroke-width="2" fill="none"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.45 1-1 1H7.5a1.5 1.5 0 0 0 0 3h9a1.5 1.5 0 0 0 0-3H15c-.55 0-1-.45-1-1v-2.34"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2z"/></svg>
        </div>
        <h3 style="font-size:18px; color:#fff; margin-bottom:8px;">Begin Your Path to Mastery</h3>
        <p style="color:var(--muted); max-width:440px; margin:0 auto 20px auto; font-size:13px;">Track your long-term practice hours toward 10,000 hours. Skills match your past and future timer sessions automatically by label or tags.</p>
        <button class="btn btn-primary" id="btn-empty-add-skill">Add Your First Skill</button>
      </div>
    </section>

    <!-- VIEW 6: SETTINGS -->
    <section class="view-container" id="view-settings">
      <div class="view-header">
        <div>
          <div class="view-title">Settings & Customization</div>
          <div class="view-desc">Configure timer intervals, sound chimes, whole-app backup, and tag taxonomies</div>
        </div>
      </div>

      <div class="settings-grid">
        <!-- CLOUD SYNC -->
        <div class="card" id="sync-card">
          <div style="font-size:16px; font-weight:700; color:#fff; margin-bottom:4px;">Cloud Sync</div>
          <div style="font-size:12px; color:var(--muted); margin-bottom:14px;">Keeps this device and your other devices in sync through your Cloudflare server. Works offline; changes upload when the server is reachable.</div>

          <div class="sync-settings-status" id="sync-settings-status" data-state="off">Sync off</div>

          <div id="sync-connect-form">
            <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin-top:12px;">
              <input type="password" class="task-input sync-input" id="sync-token-input" placeholder="Paste your sync key" autocomplete="off" spellcheck="false" />
              <button class="btn btn-primary btn-sm" id="btn-sync-connect"><span>Connect</span></button>
            </div>
            <details style="margin-top:10px; font-size:12px; color:var(--muted);">
              <summary style="cursor:pointer;">Server (advanced)</summary>
              <input type="text" class="task-input sync-input" id="sync-server-input" placeholder="Leave empty for the default server" autocomplete="off" spellcheck="false" style="margin-top:8px;" />
            </details>
            <div style="margin-top:10px; font-size:11px; color:var(--muted);">The key is stored only on this device.</div>
          </div>

          <div id="sync-connected-actions" style="display:none; margin-top:12px;">
            <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center;">
              <button class="btn btn-primary btn-sm" id="btn-sync-now"><span>Sync Now</span></button>
              <button class="btn btn-secondary btn-sm" id="btn-sync-disconnect"><span>Disconnect This Device</span></button>
            </div>
            <div style="margin-top:10px; font-size:11px; color:var(--muted);">Server: <span id="sync-server-label"></span></div>
          </div>
        </div>

        <!-- NEW WHOLE-APP BACKUP & RESTORE (TOP OF SETTINGS) -->
        <div class="card">
          <div style="font-size:16px; font-weight:700; color:#fff; margin-bottom:4px;">Whole-App Backup & Restore</div>
          <div style="font-size:12px; color:var(--muted); margin-bottom:16px;">Export or restore your complete FocusDeck database including sessions, timeblocks, skills, templates, and settings.</div>

          <div style="display:flex; gap:12px; flex-wrap:wrap; align-items:center;">
            <button class="btn btn-primary btn-sm" id="btn-backup-export-all">
              <svg viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              <span>Export All Data (.json)</span>
            </button>

            <label class="btn btn-secondary btn-sm" style="cursor:pointer; margin:0;">
              <svg viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
              <span>Import Data</span>
              <input type="file" id="backup-import-file" accept=".json" style="display:none;" />
            </label>

            <button class="btn btn-secondary btn-sm" id="btn-backup-restore-snapshot" title="Revert to snapshot taken before last import">
              <svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
              <span>Restore Last Snapshot</span>
            </button>
          </div>

          <div style="margin-top:14px; font-size:11px; color:var(--muted); display:flex; gap:20px;" id="backup-meta-timestamps">
            <span>Last export: <strong style="color:var(--text);" id="backup-last-export-time">Never</strong></span>
            <span>Last import: <strong style="color:var(--text);" id="backup-last-import-time">Never</strong></span>
          </div>
        </div>

        <!-- Timer Durations Card -->
        <div class="card">
          <div style="font-size:16px; font-weight:700; color:#fff; margin-bottom:16px;">Interval Durations (Minutes)</div>

          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-title">Focus Duration</span>
              <span class="setting-desc">Standard length of deep focus sessions</span>
            </div>
            <input type="number" class="setting-input-num" id="setting-focus-dur" min="1" max="180" />
          </div>

          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-title">Short Break</span>
              <span class="setting-desc">Rest duration between focus sessions</span>
            </div>
            <input type="number" class="setting-input-num" id="setting-short-break-dur" min="1" max="60" />
          </div>

          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-title">Long Break</span>
              <span class="setting-desc">Extended recovery after completing a cycle</span>
            </div>
            <input type="number" class="setting-input-num" id="setting-long-break-dur" min="1" max="120" />
          </div>

          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-title">Sessions per Cycle</span>
              <span class="setting-desc">Focus sessions required to trigger a long break</span>
            </div>
            <input type="number" class="setting-input-num" id="setting-sessions-cycle" min="1" max="12" />
          </div>

          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-title">Daily Focus Goal</span>
              <span class="setting-desc">Target focus minutes per day for streak progress</span>
            </div>
            <input type="number" class="setting-input-num" id="setting-daily-goal" min="10" max="1440" />
          </div>

          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-title">Daily Streak Override (Days)</span>
              <span class="setting-desc">Set custom daily streak count, or leave empty to calculate automatically from history</span>
            </div>
            <input type="number" class="setting-input-num" id="setting-daily-streak" placeholder="Auto" min="0" max="9999" />
          </div>

          <div style="margin-top:16px; display:flex; gap:10px; flex-wrap:wrap; align-items:center;">
            <span style="font-size:12px; color:var(--muted);">Quick Presets:</span>
            <button class="btn btn-secondary btn-sm preset-btn" data-preset="25-5">25 / 5m</button>
            <button class="btn btn-secondary btn-sm preset-btn" data-preset="50-10">50 / 10m</button>
            <button class="btn btn-secondary btn-sm preset-btn" data-preset="90-15">90 / 15m</button>
            <button class="btn btn-secondary btn-sm" id="btn-save-custom-preset">Save As Preset</button>
            <button class="btn btn-secondary btn-sm" id="btn-load-custom-preset" style="display:none;">Load My Preset (<span id="custom-preset-label"></span>)</button>
          </div>
        </div>

        <!-- Automation & Notification Toggles -->
        <div class="card">
          <div style="font-size:16px; font-weight:700; color:#fff; margin-bottom:16px;">Preferences & Automation</div>

          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-title">Enable Break Cycles</span>
              <span class="setting-desc">Automatically switch between focus and breaks</span>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" id="setting-enable-breaks" />
              <span class="toggle-slider"></span>
            </label>
          </div>

          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-title">Cycle Counting Dots</span>
              <span class="setting-desc">Display the 4-session cycle progress dots</span>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" id="setting-enable-counting" />
              <span class="toggle-slider"></span>
            </label>
          </div>

          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-title">Auto-Start Next Session</span>
              <span class="setting-desc">Begin the next phase automatically when timer elapses</span>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" id="setting-auto-start" />
              <span class="toggle-slider"></span>
            </label>
          </div>

          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-title">Sound Chime</span>
              <span class="setting-desc">Synthesize dual-sine bell chime at session end</span>
            </div>
            <div style="display:flex; align-items:center; gap:10px;">
              <button class="btn btn-secondary btn-sm" id="btn-test-chime">Test Chime</button>
              <label class="toggle-switch">
                <input type="checkbox" id="setting-sound" />
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>

          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-title">Desktop Notifications</span>
              <span class="setting-desc">Native browser alerts when sessions complete</span>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" id="setting-desktop-notif" />
              <span class="toggle-slider"></span>
            </label>
          </div>

          <div class="setting-row">
            <div class="setting-info">
              <span class="setting-title">Countdown in Tab Title</span>
              <span class="setting-desc">Display remaining time in browser tab</span>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" id="setting-tab-title" />
              <span class="toggle-slider"></span>
            </label>
          </div>
        </div>

        <!-- Tag Manager -->
        <div class="card">
          <div style="font-size:16px; font-weight:700; color:#fff; margin-bottom:16px;">Tag Taxonomy Manager</div>
          <div style="display:flex; gap:10px; margin-bottom:16px;">
            <input type="text" class="task-input" id="new-tag-name" placeholder="New tag name..." style="flex:1;" />
            <input type="color" id="new-tag-color" value="#4F5BF0" style="width:40px; height:40px; border-radius:8px; border:none; background:none; cursor:pointer;" />
            <button class="btn btn-primary btn-sm" id="btn-create-tag">Add Tag</button>
          </div>
          <div id="settings-tags-list" style="display:flex; flex-direction:column; gap:8px;"></div>
        </div>

        <!-- Danger Zone -->
        <div class="card" style="border-color:rgba(255,92,108,0.25);">
          <div style="font-size:16px; font-weight:700; color:var(--coral); margin-bottom:6px;">Danger Zone</div>
          <p style="font-size:13px; color:var(--muted); margin-bottom:16px;">Reset all data, history, timeblocks, and skills permanently.</p>
          <button class="btn btn-danger btn-sm" id="btn-open-clear-modal">Clear All Application Data</button>
        </div>
      </div>
    </section>
  </main>
</div>

<!-- =========================================
     MODALS
     ========================================= -->

<!-- Modal: Add / Edit Time Block -->
<div class="modal-overlay" id="modal-add-timeblock">
  <div class="modal-card">
    <div class="modal-header">
      <div class="modal-title" id="modal-tb-title">Add Time Block</div>
      <button class="modal-close-btn" id="btn-close-tb-modal">
        <svg viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    </div>
    <form id="form-add-timeblock" style="display:flex; flex-direction:column; gap:16px;">
      <input type="hidden" id="tb-input-id" value="" />
      <div>
        <label style="display:block; font-size:12px; color:var(--muted); margin-bottom:4px;">Block Label</label>
        <input type="text" class="task-input" id="tb-input-label" placeholder="e.g., Deep Architecture Work" list="recent-labels-datalist" required />
      </div>
      <div style="display:flex; gap:12px;">
        <div style="flex:1;">
          <label style="display:block; font-size:12px; color:var(--muted); margin-bottom:4px;">Duration (Minutes)</label>
          <input type="number" class="task-input" id="tb-input-dur" value="60" min="5" max="480" required />
        </div>
        <div style="width:110px;">
          <label style="display:block; font-size:12px; color:var(--muted); margin-bottom:4px;">Start Time (Optional)</label>
          <input type="time" class="task-input" id="tb-input-starttime" />
        </div>
        <div style="width:70px;">
          <label style="display:block; font-size:12px; color:var(--muted); margin-bottom:4px;">Color</label>
          <input type="color" id="tb-input-color" value="#4F5BF0" style="width:100%; height:42px; border-radius:8px; border:none; background:none; cursor:pointer;" />
        </div>
      </div>
      <div>
        <label style="display:block; font-size:12px; color:var(--muted); margin-bottom:6px;">Select Tags</label>
        <div class="tags-chips" id="tb-modal-tags-container"></div>
      </div>
      <div style="display:flex; justify-content:flex-end; gap:10px; margin-top:8px;">
        <button type="button" class="btn btn-secondary btn-sm" id="btn-cancel-tb-modal">Cancel</button>
        <button type="submit" class="btn btn-primary btn-sm">Save Block</button>
      </div>
    </form>
  </div>
</div>

<!-- Modal: Time Block Templates -->
<div class="modal-overlay" id="modal-tb-templates">
  <div class="modal-card">
    <div class="modal-header">
      <div class="modal-title" id="modal-template-title">Time Block Templates</div>
      <button class="modal-close-btn" id="btn-close-template-modal">
        <svg viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    </div>
    <div id="template-modal-content"></div>
  </div>
</div>

<!-- Modal: Add / Edit Skill (10,000 Hours) -->
<div class="modal-overlay" id="modal-add-skill">
  <div class="modal-card">
    <div class="modal-header">
      <div class="modal-title" id="modal-skill-title">Add Mastery Skill</div>
      <button class="modal-close-btn" id="btn-close-skill-modal">
        <svg viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    </div>
    <form id="form-add-skill" style="display:flex; flex-direction:column; gap:16px;">
      <input type="hidden" id="skill-input-id" value="" />
      <div>
        <label style="display:block; font-size:12px; color:var(--muted); margin-bottom:4px;">Skill Name</label>
        <input type="text" class="task-input" id="skill-input-name" placeholder="e.g., Software Engineering, Piano, Writing..." required />
      </div>
      <div style="display:flex; gap:12px;">
        <div style="flex:1;">
          <label style="display:block; font-size:12px; color:var(--muted); margin-bottom:4px;">Goal Hours</label>
          <input type="number" class="task-input" id="skill-input-goal" value="10000" min="10" max="50000" required />
        </div>
        <div style="width:80px;">
          <label style="display:block; font-size:12px; color:var(--muted); margin-bottom:4px;">Color</label>
          <input type="color" id="skill-input-color" value="#4F5BF0" style="width:100%; height:42px; border-radius:8px; border:none; background:none; cursor:pointer;" />
        </div>
      </div>
      <div>
        <label style="display:block; font-size:12px; color:var(--muted); margin-bottom:4px;">Link Focus Tags (Retroactively counted)</label>
        <div class="tags-chips" id="skill-link-tags-container"></div>
      </div>
      <div>
        <label style="display:block; font-size:12px; color:var(--muted); margin-bottom:4px;">Link Task Labels (Retroactively counted)</label>
        <div style="max-height:110px; overflow-y:auto; border:1px solid var(--border); border-radius:8px; padding:8px; background:var(--surface-2);" id="skill-link-labels-container"></div>
      </div>
      <div style="display:flex; justify-content:flex-end; gap:10px; margin-top:8px;">
        <button type="button" class="btn btn-secondary btn-sm" id="btn-cancel-skill-modal">Cancel</button>
        <button type="submit" class="btn btn-primary btn-sm">Save Skill</button>
      </div>
    </form>
  </div>
</div>

<!-- Modal: Skill Detail Panel -->
<div class="modal-overlay" id="modal-skill-detail">
  <div class="modal-card modal-card-lg" style="max-height:90vh; overflow-y:auto;">
    <div class="modal-header">
      <div style="display:flex; align-items:center; gap:10px;">
        <span class="tb-color-dot" id="detail-skill-color" style="width:14px; height:14px;"></span>
        <div class="modal-title" id="detail-skill-title">Skill Mastery Detail</div>
      </div>
      <button class="modal-close-btn" id="btn-close-skill-detail">
        <svg viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    </div>
    <div id="detail-skill-content"></div>
  </div>
</div>

<!-- Modal: Add Historical Backlog Hours -->
<div class="modal-overlay" id="modal-add-backlog">
  <div class="modal-card">
    <div class="modal-header">
      <div class="modal-title">Add Historical Practice Hours</div>
      <button class="modal-close-btn" id="btn-close-backlog-modal">
        <svg viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    </div>
    <form id="form-add-backlog" style="display:flex; flex-direction:column; gap:14px;">
      <input type="hidden" id="backlog-skill-id" value="" />
      <div>
        <label style="display:block; font-size:12px; color:var(--muted); margin-bottom:4px;">Hours to Credit</label>
        <input type="number" step="0.5" class="task-input" id="backlog-hours-input" placeholder="e.g., 50" min="0.5" required />
      </div>
      <div>
        <label style="display:block; font-size:12px; color:var(--muted); margin-bottom:4px;">Note / Origin</label>
        <input type="text" class="task-input" id="backlog-note-input" placeholder="e.g., College coursework, past notebook logs..." />
      </div>
      <div style="display:flex; justify-content:flex-end; gap:10px; margin-top:8px;">
        <button type="button" class="btn btn-secondary btn-sm" id="btn-cancel-backlog">Cancel</button>
        <button type="submit" class="btn btn-primary btn-sm">Add Backlog Hours</button>
      </div>
    </form>
  </div>
</div>

<!-- Modal: Whole-App Backup Import Confirmation -->
<div class="modal-overlay" id="modal-backup-import">
  <div class="modal-card">
    <div class="modal-header">
      <div class="modal-title">Import FocusDeck Backup</div>
      <button class="modal-close-btn" id="btn-close-backup-modal">
        <svg viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    </div>
    <div style="font-size:13px; color:var(--text); margin-bottom:16px;">
      A valid FocusDeck backup file was selected. A safety snapshot of your current state will be automatically created before applying any changes.
    </div>
    <div class="card" style="background:var(--surface-2); padding:16px; margin-bottom:20px;" id="backup-import-summary">
      <!-- Counts populated by JS -->
    </div>
    <div style="display:flex; flex-direction:column; gap:10px;">
      <button class="btn btn-primary" id="btn-confirm-import-merge">
        <span>Merge Data</span>
        <span style="font-size:11px; font-weight:normal; opacity:0.85;">(Keep existing, add new records, keep newer on conflicts)</span>
      </button>
      <button class="btn btn-danger" id="btn-confirm-import-replace">
        <span>Replace Everything</span>
        <span style="font-size:11px; font-weight:normal; opacity:0.85;">(Wipes current state and loads backup exactly)</span>
      </button>
      <button class="btn btn-secondary btn-sm" id="btn-cancel-backup-import" style="margin-top:6px;">Cancel</button>
    </div>
  </div>
</div>

<!-- Modal: Manual Session Entry -->
<div class="modal-overlay" id="modal-manual-entry">
  <div class="modal-card">
    <div class="modal-header">
      <div class="modal-title" id="modal-manual-title">Add Manual Session</div>
      <button class="modal-close-btn" id="btn-close-manual-modal">
        <svg viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    </div>
    <form id="form-manual-entry" style="display:flex; flex-direction:column; gap:14px;">
      <input type="hidden" id="manual-input-id" value="" />
      <div>
        <label style="display:block; font-size:12px; color:var(--muted); margin-bottom:4px;">Task Label</label>
        <input type="text" class="task-input" id="manual-input-label" placeholder="e.g., Code Review" list="recent-labels-datalist" required />
      </div>
      <div style="display:flex; gap:12px;">
        <div style="flex:1;">
          <label style="display:block; font-size:12px; color:var(--muted); margin-bottom:4px;">Mode</label>
          <select class="tb-time-input" id="manual-input-mode" style="width:100%; padding:10px;">
            <option value="focus">Focus</option>
            <option value="shortBreak">Short Break</option>
            <option value="longBreak">Long Break</option>
          </select>
        </div>
        <div style="flex:1;">
          <label style="display:block; font-size:12px; color:var(--muted); margin-bottom:4px;">Duration (Minutes)</label>
          <input type="number" class="task-input" id="manual-input-dur" value="25" min="1" max="360" required />
        </div>
      </div>
      <div>
        <label style="display:block; font-size:12px; color:var(--muted); margin-bottom:4px;">Date & Start Time</label>
        <input type="datetime-local" class="task-input" id="manual-input-datetime" required />
      </div>
      <div>
        <label style="display:block; font-size:12px; color:var(--muted); margin-bottom:4px;">Note</label>
        <input type="text" class="task-input" id="manual-input-note" placeholder="Optional notes..." />
      </div>
      <div style="display:flex; justify-content:flex-end; gap:10px; margin-top:8px;">
        <button type="button" class="btn btn-secondary btn-sm" id="btn-cancel-manual">Cancel</button>
        <button type="submit" class="btn btn-primary btn-sm">Save Session</button>
      </div>
    </form>
  </div>
</div>

<!-- Modal: Clear Data Confirmation -->
<div class="modal-overlay" id="modal-clear-data">
  <div class="modal-card">
    <div class="modal-header">
      <div class="modal-title" style="color:var(--coral);">Wipe All Data Permanently</div>
      <button class="modal-close-btn" id="btn-close-clear-modal">
        <svg viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    </div>
    <p style="font-size:13px; color:var(--muted); margin-bottom:16px;">This action cannot be undone. Type <strong style="color:#fff;">DELETE</strong> to wipe all stored sessions, timeblocks, and skills.</p>
    <input type="text" class="task-input" id="confirm-delete-input" placeholder="Type DELETE to confirm..." style="margin-bottom:16px;" />
    <div style="display:flex; justify-content:flex-end; gap:10px;">
      <button type="button" class="btn btn-secondary btn-sm" id="btn-cancel-clear">Cancel</button>
      <button type="button" class="btn btn-danger btn-sm" id="btn-confirm-wipe" disabled>Wipe Data</button>
    </div>
  </div>
</div>

<!-- Modal: In-App Confirmation Dialog (Iframe Safe) -->
<div class="modal-overlay" id="modal-confirm">
  <div class="modal-card" style="max-width:440px;">
    <div class="modal-header">
      <div class="modal-title" id="confirm-modal-title">Confirm Action</div>
      <button class="modal-close-btn" id="btn-close-confirm-modal">
        <svg viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    </div>
    <div id="confirm-modal-body" style="font-size:13px; color:var(--text); line-height:1.5; margin-bottom:20px;">Are you sure?</div>
    <div style="display:flex; justify-content:flex-end; gap:10px;">
      <button class="btn btn-secondary btn-sm" id="btn-confirm-cancel">Cancel</button>
      <button class="btn btn-primary btn-sm" id="btn-confirm-ok">Confirm</button>
    </div>
  </div>
</div>

<!-- Modal: Keyboard Shortcuts Cheat Sheet -->
<div class="modal-overlay" id="modal-shortcuts">
  <div class="modal-card">
    <div class="modal-header">
      <div class="modal-title">Keyboard Shortcuts</div>
      <button class="modal-close-btn" id="btn-close-shortcuts-modal">
        <svg viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    </div>
    <div style="display:flex; flex-direction:column; gap:10px; font-size:13px;">
      <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid var(--border);">
        <span style="color:#fff;">Space</span><span style="color:var(--muted);">Start / Pause Timer (Timer view only)</span>
      </div>
      <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid var(--border);">
        <span style="color:#fff;">R</span><span style="color:var(--muted);">Reset Timer (Timer view only)</span>
      </div>
      <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid var(--border);">
        <span style="color:#fff;">S</span><span style="color:var(--muted);">Skip to Next Session (Timer view only)</span>
      </div>
      <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid var(--border);">
        <span style="color:#fff;">L</span><span style="color:var(--muted);">Focus Task Input (Timer view only)</span>
      </div>
      <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid var(--border);">
        <span style="color:#fff;">1</span><span style="color:var(--muted);">Switch to Timer View</span>
      </div>
      <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid var(--border);">
        <span style="color:#fff;">2</span><span style="color:var(--muted);">Switch to Time Block View</span>
      </div>
      <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid var(--border);">
        <span style="color:#fff;">3</span><span style="color:var(--muted);">Switch to Log View</span>
      </div>
      <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid var(--border);">
        <span style="color:#fff;">4</span><span style="color:var(--muted);">Switch to Reports View</span>
      </div>
      <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid var(--border);">
        <span style="color:#fff;">5</span><span style="color:var(--muted);">Switch to 10,000 Hours View</span>
      </div>
      <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid var(--border);">
        <span style="color:#fff;">6</span><span style="color:var(--muted);">Switch to Settings View</span>
      </div>
      <div style="display:flex; justify-content:space-between; padding:6px 0;">
        <span style="color:#fff;">Esc</span><span style="color:var(--muted);">Close active dialog / modal</span>
      </div>
    </div>
  </div>
</div>

<!-- Floating Shortcuts Help Button -->
<button id="btn-open-shortcuts" title="Keyboard Shortcuts (?)">?</button>

<!-- Away Banner -->
<div id="away-banner">
  <svg viewBox="0 0 24 24" width="20" height="20" stroke="var(--teal)" stroke-width="2" fill="none"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
  <span id="away-banner-text">A focus session completed while you were away!</span>
  <button class="btn btn-secondary btn-sm" id="away-dismiss-btn" style="padding:4px 8px; font-size:11px;">Dismiss</button>
</div>

<!-- Toast Container -->
<div id="toast-container"></div>
"""
