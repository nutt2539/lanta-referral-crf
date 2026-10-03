# -*- coding: utf-8 -*-
import sys

def get_css():
    return """
        :root {
            --app-max-width: 1680px;
            --primary: #1e3a8a;
            --primary-light: #3b82f6;
            --primary-dark: #0f172a;
            --accent: #0284c7;
            --bg-page: #f1f5f9;
            --card-bg: #ffffff;
            --border-color: #cbd5e1;
            --table-header: #f8fafc;
            --highlight-bg: #eff6ff;
            --calc-bg: #e0f2fe;
            --success-bg: #dcfce7;
            --success-text: #15803d;
            --danger-bg: #fee2e2;
            --danger-text: #b91c1c;
            --text-main: #1e293b;
            --text-muted: #64748b;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'TH Sarabun New', 'TH Sarabun PSK', Sarabun, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        body {
            background-color: var(--bg-page);
            color: var(--text-main);
            font-size: 14.5px;
            line-height: 1.35;
            padding-bottom: 65px;
            transition: all 0.2s ease;
        }

        /* Top Sticky Toolbar */
        .top-navbar {
            position: sticky;
            top: 0;
            z-index: 1000;
            background: #ffffff;
            border-bottom: 2px solid #cbd5e1;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            padding: 6px 18px;
        }

        .navbar-content {
            max-width: var(--app-max-width);
            width: 96%;
            margin: 0 auto;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
        }

        .nav-title-group h1 {
            font-size: 17px;
            font-weight: 700;
            color: var(--primary);
            line-height: 1.2;
        }

        .nav-title-group p {
            font-size: 12px;
            color: var(--text-muted);
        }

        .nav-actions {
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            font-size: 14px;
            font-weight: 600;
            border-radius: 6px;
            cursor: pointer;
            border: 1px solid transparent;
            transition: all 0.15s ease-in-out;
        }

        .btn-primary {
            background-color: var(--primary);
            color: #ffffff;
        }
        .btn-primary:hover {
            background-color: #172554;
        }

        .btn-success {
            background-color: #16a34a;
            border-color: #16a34a;
            color: #ffffff;
        }
        .btn-success:hover {
            background-color: #15803d;
            border-color: #15803d;
        }

        .btn-blue {
            background-color: #0284c7;
            border-color: #0284c7;
            color: #ffffff;
        }
        .btn-blue:hover {
            background-color: #0369a1;
            border-color: #0369a1;
        }

        .btn-outline {
            background-color: #ffffff;
            border-color: #cbd5e1;
            color: var(--text-main);
        }
        .btn-outline:hover {
            background-color: #f8fafc;
            border-color: #94a3b8;
        }

        .save-status {
            font-size: 12px;
            color: var(--success-text);
            background: var(--success-bg);
            padding: 4px 8px;
            border-radius: 4px;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            font-weight: 600;
        }

        /* Tabs Navigation Base */
        .tab-bar-container {
            max-width: var(--app-max-width);
            width: 96%;
            margin: 10px auto 0 auto;
            padding: 0 10px;
        }

        .tab-bar {
            display: flex;
            gap: 4px;
            border-bottom: 2px solid #cbd5e1;
            background: #ffffff;
            border-radius: 8px 8px 0 0;
            padding: 4px 6px 0 6px;
        }

        .tab-btn {
            flex: 1;
            padding: 8px 10px;
            text-align: center;
            font-size: 14px;
            font-weight: 700;
            color: #64748b;
            background: transparent;
            border: none;
            border-bottom: 4px solid transparent;
            cursor: pointer;
            transition: all 0.2s ease-in-out;
            border-radius: 6px 6px 0 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 2px;
        }

        .tab-badge {
            font-size: 11.5px;
            font-weight: 700;
            padding: 1px 8px;
            border-radius: 999px;
            transition: all 0.2s ease;
        }

        /* Distinct Tab Colors */
        /* Tab 1: Sapphire Blue */
        .tab-btn.tab-form1 .tab-badge {
            background: #dbeafe;
            color: #1e40af;
            border: 1px solid #bfdbfe;
        }
        .tab-btn.tab-form1:hover {
            background: #eff6ff;
            color: #1e40af;
        }
        .tab-btn.tab-form1.active {
            color: #1e3a8a;
            background: #eff6ff;
            border-bottom: 4px solid #1e40af;
        }
        .tab-btn.tab-form1.active .tab-badge {
            background: #1e40af;
            color: #ffffff;
            border-color: #1e40af;
            box-shadow: 0 2px 4px rgba(30, 64, 175, 0.25);
        }

        /* Tab 2: Ocean Marine Teal */
        .tab-btn.tab-form2 .tab-badge {
            background: #ccfbf1;
            color: #0f766e;
            border: 1px solid #99f6e4;
        }
        .tab-btn.tab-form2:hover {
            background: #f0fdfa;
            color: #0f766e;
        }
        .tab-btn.tab-form2.active {
            color: #115e59;
            background: #f0fdfa;
            border-bottom: 4px solid #0f766e;
        }
        .tab-btn.tab-form2.active .tab-badge {
            background: #0f766e;
            color: #ffffff;
            border-color: #0f766e;
            box-shadow: 0 2px 4px rgba(15, 118, 110, 0.25);
        }

        /* Tab 3: Royal Purple / Indigo */
        .tab-btn.tab-form3 .tab-badge {
            background: #f3e8ff;
            color: #7e22ce;
            border: 1px solid #e9d5ff;
        }
        .tab-btn.tab-form3:hover {
            background: #faf5ff;
            color: #7e22ce;
        }
        .tab-btn.tab-form3.active {
            color: #581c87;
            background: #faf5ff;
            border-bottom: 4px solid #7e22ce;
        }
        .tab-btn.tab-form3.active .tab-badge {
            background: #7e22ce;
            color: #ffffff;
            border-color: #7e22ce;
            box-shadow: 0 2px 4px rgba(126, 34, 206, 0.25);
        }

        /* Tab 4: Medical Crimson / Ruby */
        .tab-btn.tab-form4 .tab-badge {
            background: #ffe4e6;
            color: #b91c1c;
            border: 1px solid #fecdd3;
        }
        .tab-btn.tab-form4:hover {
            background: #fff1f2;
            color: #b91c1c;
        }
        .tab-btn.tab-form4.active {
            color: #881337;
            background: #fff1f2;
            border-bottom: 4px solid #b91c1c;
        }
        .tab-btn.tab-form4.active .tab-badge {
            background: #b91c1c;
            color: #ffffff;
            border-color: #b91c1c;
            box-shadow: 0 2px 4px rgba(185, 28, 28, 0.25);
        }

        /* Main Document Wrapper */
        .main-container {
            max-width: var(--app-max-width);
            width: 96%;
            margin: 0 auto 20px auto;
            padding: 0 10px;
        }

        .crf-page {
            background: #ffffff;
            padding: 16px 24px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            border: 1px solid #cbd5e1;
            border-top: none;
            display: none;
        }

        .crf-page.active {
            display: block;
        }

        /* Document Header Styling Matching PDF */
        .doc-header-box {
            background-color: var(--primary);
            color: #ffffff;
            text-align: center;
            padding: 8px 16px;
            margin-bottom: 10px;
            border-radius: 6px;
        }

        .doc-header-box h2 {
            font-size: 16.5px;
            font-weight: 700;
            letter-spacing: 0.3px;
            margin-bottom: 2px;
            line-height: 1.2;
        }

        .doc-header-box h3 {
            font-size: 14.5px;
            font-weight: 600;
            margin-bottom: 2px;
            line-height: 1.2;
        }

        .doc-header-box p {
            font-size: 12.5px;
            font-weight: 400;
            opacity: 0.95;
            font-style: italic;
            line-height: 1.2;
        }

        /* Section Header */
        .section-header {
            font-size: 15px;
            font-weight: 700;
            color: #0f172a;
            margin: 12px 0 6px 0;
            border-left: 4px solid var(--primary);
            padding: 3px 8px;
            line-height: 1.2;
        }

        /* Tables Matching PDF Layout */
        .crf-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 8px;
            font-size: 14px;
            line-height: 1.3;
        }

        .crf-table th, .crf-table td {
            border: 1px solid #94a3b8;
            padding: 4px 7px;
            vertical-align: middle;
        }

        .crf-table th {
            background-color: #f1f5f9;
            font-weight: 700;
            color: #0f172a;
            text-align: left;
            padding: 5px 7px;
        }

        .th-center, .td-center {
            text-align: center !important;
        }

        .bg-light-blue {
            background-color: #f8fafc;
        }

        .bg-highlight {
            background-color: #eff6ff;
        }

        /* Inputs */
        input[type="text"], input[type="number"], select, input[type="date"], input[type="time"] {
            width: 100%;
            padding: 3px 6px;
            font-size: 13.5px;
            border: 1px solid #cbd5e1;
            border-radius: 4px;
            color: #0f172a;
            background: #ffffff;
            height: 28px;
        }

        input[type="text"]:focus, input[type="number"]:focus, select:focus, input[type="date"]:focus, input[type="time"]:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 2px rgba(30, 58, 138, 0.15);
        }

        .input-inline {
            display: inline-block;
            width: auto;
            min-width: 80px;
        }

        .input-calc {
            background-color: var(--calc-bg) !important;
            font-weight: 700 !important;
            color: #0369a1 !important;
            border-color: #7dd3fc !important;
        }

        .badge-calc {
            display: inline-block;
            background: var(--calc-bg);
            color: #0369a1;
            font-weight: 700;
            font-size: 13px;
            padding: 2px 8px;
            border-radius: 4px;
            border: 1px solid #bae6fd;
            margin-left: 4px;
        }

        .badge-evaluated {
            font-size: 12px;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 4px;
        }
        .badge-ontime {
            background: var(--success-bg);
            color: var(--success-text);
        }
        .badge-delay {
            background: var(--danger-bg);
            color: var(--danger-text);
        }

        /* Checkbox & Radio */
        .check-group {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        .check-row {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            align-items: center;
        }

        .form-check {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            cursor: pointer;
            user-select: none;
        }

        .form-check input[type="checkbox"], .form-check input[type="radio"] {
            cursor: pointer;
            width: 16px;
            height: 16px;
            accent-color: var(--primary);
        }

        /* Verification Box */
        .verification-box {
            margin-top: 25px;
            border: 1px solid #94a3b8;
            padding: 15px;
            background: #fafafa;
        }

        .signature-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .sign-field {
            margin-top: 8px;
        }

        .sign-line {
            display: inline-block;
            border-bottom: 1px dotted #475569;
            width: 200px;
            margin-left: 5px;
        }

        .pdpa-note {
            font-size: 12px;
            color: #64748b;
            margin-top: 15px;
            font-style: italic;
            border-top: 1px solid #e2e8f0;
            padding-top: 8px;
        }

        /* Bottom Floating Bar */
        .bottom-nav-bar {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: #ffffff;
            border-top: 1px solid #cbd5e1;
            padding: 6px 18px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 -4px 6px -1px rgba(0, 0, 0, 0.05);
            z-index: 999;
            height: 50px;
        }

        .bottom-nav-content {
            max-width: var(--app-max-width);
            width: 96%;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        /* ==========================================================================
           FOUR DISTINCT CLINICAL COLOR THEMES (Forms 1 - 4)
           ========================================================================== */

        /* ---------------- Theme 1: Sapphire Blue (Form 1) ---------------- */
        .theme-form1 {
            border-top: 5px solid #1e40af !important;
            border-left: 1px solid #bfdbfe;
            border-right: 1px solid #bfdbfe;
            border-bottom: 1px solid #bfdbfe;
            box-shadow: 0 4px 20px rgba(30, 64, 175, 0.08);
        }
        .theme-form1 .doc-header-box {
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%) !important;
            box-shadow: 0 4px 12px rgba(30, 64, 175, 0.25);
            border-radius: 6px;
        }
        .theme-form1 .section-header {
            color: #1e3a8a !important;
            border-left: 5px solid #1e40af !important;
            background: linear-gradient(90deg, #eff6ff 0%, rgba(239, 246, 255, 0) 100%);
            padding: 6px 12px;
            border-radius: 0 4px 4px 0;
        }
        .theme-form1 .crf-table th {
            background-color: #eff6ff !important;
            color: #1e3a8a !important;
            border-color: #bfdbfe;
        }
        .theme-form1 .crf-table td {
            border-color: #cbd5e1;
        }
        .theme-form1 .crf-table td[style*="background: #f8fafc"],
        .theme-form1 .crf-table td[style*="background:#f8fafc"] {
            background-color: #f0f7ff !important;
            color: #1e3a8a;
        }
        .theme-form1 input[type="text"]:focus,
        .theme-form1 input[type="number"]:focus,
        .theme-form1 select:focus,
        .theme-form1 input[type="date"]:focus,
        .theme-form1 input[type="time"]:focus {
            border-color: #2563eb;
            box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
        }
        .theme-form1 .form-check input[type="checkbox"],
        .theme-form1 .form-check input[type="radio"] {
            accent-color: #1e40af !important;
        }
        .theme-form1 .input-calc {
            background-color: #eff6ff !important;
            color: #1e40af !important;
            border-color: #93c5fd !important;
        }
        .theme-form1 .badge-calc {
            background: #dbeafe !important;
            color: #1e40af !important;
            border: 1px solid #93c5fd !important;
        }
        .theme-form1 .study-id-sync {
            color: #1e40af !important;
            font-weight: 700;
        }

        /* ---------------- Theme 2: Ocean Marine Teal (Form 2) ---------------- */
        .theme-form2 {
            border-top: 5px solid #0f766e !important;
            border-left: 1px solid #99f6e4;
            border-right: 1px solid #99f6e4;
            border-bottom: 1px solid #99f6e4;
            box-shadow: 0 4px 20px rgba(15, 118, 110, 0.08);
        }
        .theme-form2 .doc-header-box {
            background: linear-gradient(135deg, #134e4a 0%, #0d9488 100%) !important;
            box-shadow: 0 4px 12px rgba(15, 118, 110, 0.25);
            border-radius: 6px;
        }
        .theme-form2 .section-header {
            color: #0f766e !important;
            border-left: 5px solid #0f766e !important;
            background: linear-gradient(90deg, #f0fdfa 0%, rgba(240, 253, 250, 0) 100%);
            padding: 6px 12px;
            border-radius: 0 4px 4px 0;
        }
        .theme-form2 .crf-table th {
            background-color: #f0fdfa !important;
            color: #115e59 !important;
            border-color: #99f6e4;
        }
        .theme-form2 .crf-table td {
            border-color: #cbd5e1;
        }
        .theme-form2 .crf-table td[style*="background: #f8fafc"],
        .theme-form2 .crf-table td[style*="background:#f8fafc"] {
            background-color: #f0fdfa !important;
            color: #134e4a;
        }
        .theme-form2 .crf-table td[style*="background: #eff6ff"],
        .theme-form2 .crf-table td[style*="background:#eff6ff"] {
            background-color: #e6fffa !important;
        }
        .theme-form2 input[type="text"]:focus,
        .theme-form2 input[type="number"]:focus,
        .theme-form2 select:focus,
        .theme-form2 input[type="date"]:focus,
        .theme-form2 input[type="time"]:focus {
            border-color: #0d9488;
            box-shadow: 0 0 0 2px rgba(13, 148, 136, 0.2);
        }
        .theme-form2 .form-check input[type="checkbox"],
        .theme-form2 .form-check input[type="radio"] {
            accent-color: #0f766e !important;
        }
        .theme-form2 .input-calc {
            background-color: #f0fdfa !important;
            color: #0f766e !important;
            border-color: #5eead4 !important;
        }
        .theme-form2 .badge-calc {
            background: #ccfbf1 !important;
            color: #0f766e !important;
            border: 1px solid #5eead4 !important;
        }
        .theme-form2 .study-id-sync {
            color: #0f766e !important;
            font-weight: 700;
        }

        /* ---------------- Theme 3: Royal Purple / Indigo (Form 3) ---------------- */
        .theme-form3 {
            border-top: 5px solid #7e22ce !important;
            border-left: 1px solid #e9d5ff;
            border-right: 1px solid #e9d5ff;
            border-bottom: 1px solid #e9d5ff;
            box-shadow: 0 4px 20px rgba(126, 34, 206, 0.08);
        }
        .theme-form3 .doc-header-box {
            background: linear-gradient(135deg, #3b0764 0%, #7e22ce 100%) !important;
            box-shadow: 0 4px 12px rgba(126, 34, 206, 0.25);
            border-radius: 6px;
        }
        .theme-form3 .section-header {
            color: #581c87 !important;
            border-left: 5px solid #7e22ce !important;
            background: linear-gradient(90deg, #faf5ff 0%, rgba(250, 245, 255, 0) 100%);
            padding: 6px 12px;
            border-radius: 0 4px 4px 0;
        }
        .theme-form3 .crf-table th {
            background-color: #faf5ff !important;
            color: #581c87 !important;
            border-color: #e9d5ff;
        }
        .theme-form3 .crf-table td {
            border-color: #cbd5e1;
        }
        .theme-form3 .crf-table td[style*="background: #f8fafc"],
        .theme-form3 .crf-table td[style*="background:#f8fafc"] {
            background-color: #faf5ff !important;
            color: #581c87;
        }
        .theme-form3 input[type="text"]:focus,
        .theme-form3 input[type="number"]:focus,
        .theme-form3 select:focus,
        .theme-form3 input[type="date"]:focus,
        .theme-form3 input[type="time"]:focus {
            border-color: #7e22ce;
            box-shadow: 0 0 0 2px rgba(126, 34, 206, 0.2);
        }
        .theme-form3 .form-check input[type="checkbox"],
        .theme-form3 .form-check input[type="radio"] {
            accent-color: #7e22ce !important;
        }
        .theme-form3 .input-calc {
            background-color: #faf5ff !important;
            color: #6b21a8 !important;
            border-color: #d8b4fe !important;
        }
        .theme-form3 .badge-calc {
            background: #f3e8ff !important;
            color: #6b21a8 !important;
            border: 1px solid #d8b4fe !important;
        }
        .theme-form3 .study-id-sync {
            color: #7e22ce !important;
            font-weight: 700;
        }

        /* ---------------- Theme 4: Medical Crimson / Ruby (Form 4) ---------------- */
        .theme-form4 {
            border-top: 5px solid #b91c1c !important;
            border-left: 1px solid #fecdd3;
            border-right: 1px solid #fecdd3;
            border-bottom: 1px solid #fecdd3;
            box-shadow: 0 4px 20px rgba(185, 28, 28, 0.08);
        }
        .theme-form4 .doc-header-box {
            background: linear-gradient(135deg, #7f1d1d 0%, #be123c 100%) !important;
            box-shadow: 0 4px 12px rgba(185, 28, 28, 0.25);
            border-radius: 6px;
        }
        .theme-form4 .section-header {
            color: #991b1b !important;
            border-left: 5px solid #b91c1c !important;
            background: linear-gradient(90deg, #fff1f2 0%, rgba(255, 241, 242, 0) 100%);
            padding: 6px 12px;
            border-radius: 0 4px 4px 0;
        }
        .theme-form4 .crf-table th {
            background-color: #fff1f2 !important;
            color: #881337 !important;
            border-color: #fecdd3;
        }
        .theme-form4 .crf-table td {
            border-color: #cbd5e1;
        }
        .theme-form4 .crf-table td[style*="background: #f8fafc"],
        .theme-form4 .crf-table td[style*="background:#f8fafc"] {
            background-color: #fff1f2 !important;
            color: #881337;
        }
        .theme-form4 input[type="text"]:focus,
        .theme-form4 input[type="number"]:focus,
        .theme-form4 select:focus,
        .theme-form4 input[type="date"]:focus,
        .theme-form4 input[type="time"]:focus {
            border-color: #b91c1c;
            box-shadow: 0 0 0 2px rgba(185, 28, 28, 0.2);
        }
        .theme-form4 .form-check input[type="checkbox"],
        .theme-form4 .form-check input[type="radio"] {
            accent-color: #b91c1c !important;
        }
        .theme-form4 .input-calc {
            background-color: #fff1f2 !important;
            color: #991b1b !important;
            border-color: #fda4af !important;
        }
        .theme-form4 .badge-calc {
            background: #ffe4e6 !important;
            color: #991b1b !important;
            border: 1px solid #fda4af !important;
        }
        .theme-form4 .study-id-sync {
            color: #b91c1c !important;
            font-weight: 700;
        }

        /* Dynamic Next Button Styles matching Form Themes */
        .btn-theme-1 { background-color: #1e40af !important; color: #ffffff !important; }
        .btn-theme-1:hover { background-color: #1e3a8a !important; }
        .btn-theme-2 { background-color: #0f766e !important; color: #ffffff !important; }
        .btn-theme-2:hover { background-color: #115e59 !important; }
        .btn-theme-3 { background-color: #7e22ce !important; color: #ffffff !important; }
        .btn-theme-3:hover { background-color: #6b21a8 !important; }
        .btn-theme-4 { background-color: #b91c1c !important; color: #ffffff !important; }
        .btn-theme-4:hover { background-color: #991b1b !important; }

        /* ==========================================================================
           AUTOMATIC RESPONSIVE SCREEN ADAPTATION (Windows Browser & Large Monitors)
           Auto-adjusts density, padding, and layout fluidly with zero manual toggle
           ========================================================================== */
        /* Fluid Large-Screen Proportions */
        @media screen and (min-width: 1024px) {
            .navbar-content,
            .tab-bar-container,
            .main-container,
            .bottom-nav-content {
                max-width: 98% !important;
                width: 98% !important;
            }
            .crf-page {
                padding: 12px 20px !important;
            }
            .doc-header-box {
                padding: 6px 14px !important;
                margin-bottom: 8px !important;
            }
            .section-header {
                font-size: 14px !important;
                margin: 8px 0 4px 0 !important;
                padding: 3px 8px !important;
            }
            .crf-table {
                margin-bottom: 6px !important;
                font-size: 13.5px !important;
            }
            .crf-table th,
            .crf-table td {
                padding: 4px 8px !important;
            }
            input[type="text"],
            input[type="number"],
            select,
            input[type="date"],
            input[type="time"] {
                height: 28px !important;
                padding: 2px 6px !important;
                font-size: 13px !important;
            }
        }

        /* Compact Auto-Fit on typical Windows browser windows (with toolbars / taskbar) or laptops */
        @media screen and (max-height: 860px) {
            body {
                font-size: 13.5px !important;
                line-height: 1.25 !important;
                padding-bottom: 50px !important;
            }
            .top-navbar {
                padding: 4px 14px !important;
            }
            .nav-title-group h1 {
                font-size: 15px !important;
            }
            .nav-title-group p {
                font-size: 11px !important;
            }
            .crf-page {
                padding: 8px 16px !important;
            }
            .doc-header-box {
                padding: 4px 10px !important;
                margin-bottom: 6px !important;
            }
            .doc-header-box h2 {
                font-size: 14px !important;
            }
            .doc-header-box h3 {
                font-size: 12.5px !important;
            }
            .doc-header-box p {
                font-size: 11px !important;
            }
            .section-header {
                font-size: 13px !important;
                margin: 6px 0 3px 0 !important;
                padding: 2px 6px !important;
            }
            .crf-table {
                margin-bottom: 4px !important;
                font-size: 12.5px !important;
            }
            .crf-table th,
            .crf-table td {
                padding: 2.5px 6px !important;
            }
            input[type="text"],
            input[type="number"],
            select,
            input[type="date"],
            input[type="time"] {
                height: 25px !important;
                padding: 1px 5px !important;
                font-size: 12px !important;
            }
            .tab-btn {
                padding: 5px 8px !important;
                font-size: 12.5px !important;
            }
            .form-check {
                font-size: 12px !important;
            }
        }

        /* Ultra-wide / 4K Desktop Monitors */
        @media screen and (min-width: 1800px) {
            .navbar-content,
            .tab-bar-container,
            .main-container,
            .bottom-nav-content {
                max-width: 1760px !important;
            }
        }

        /* Dynamic Auto-Compact Utility Classes */
        body.auto-compact .crf-table th,
        body.auto-compact .crf-table td {
            padding: 2.5px 6px !important;
        }

        /* ==========================================================================
           ADMIN DASHBOARD & MODAL STYLES
           ========================================================================== */
        .btn-admin {
            background-color: #3b0764 !important;
            color: #ffffff !important;
            border: 1px solid #581c87 !important;
        }
        .btn-admin:hover {
            background-color: #581c87 !important;
        }

        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(4px);
            z-index: 2000;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .modal-box {
            background: #ffffff;
            border-radius: 8px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.25), 0 10px 10px -5px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 440px;
            overflow: hidden;
            border: 1px solid #cbd5e1;
            animation: modalFadeIn 0.2s ease-out;
        }

        .modal-box-large {
            max-width: 1400px;
            width: 96%;
        }

        @keyframes modalFadeIn {
            from { opacity: 0; transform: scale(0.97); }
            to { opacity: 1; transform: scale(1); }
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 18px;
            border-bottom: 1px solid #e2e8f0;
            background: #f8fafc;
        }

        .modal-close-btn {
            background: transparent;
            border: none;
            font-size: 18px;
            cursor: pointer;
            color: #64748b;
            padding: 4px 8px;
            border-radius: 4px;
            line-height: 1;
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }
        .modal-close-btn:hover {
            background: rgba(0,0,0,0.08);
            color: #0f172a;
        }

        .admin-case-row:hover {
            background-color: #f1f5f9;
        }

        /* ==========================================================================
           PRINT & INDIVIDUAL PATIENT PDF EXPORT STYLES
           ========================================================================== */
        @media print {
            @page {
                size: A4 portrait;
                margin: 10mm 12mm;
            }

            html, body {
                background: #ffffff !important;
                color: #0f172a !important;
                font-size: 11.5px !important;
                line-height: 1.25 !important;
                padding: 0 !important;
                margin: 0 !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }

            .top-navbar, .tab-bar-container, .bottom-nav-bar, .btn, .modal-overlay, #save-status {
                display: none !important;
            }

            .main-container {
                max-width: 100% !important;
                width: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
            }

            /* Default: print all 4 forms sequentially */
            body:not(.print-single-tab) .crf-page {
                display: block !important;
                page-break-after: always !important;
                break-after: page !important;
                border: none !important;
                box-shadow: none !important;
                padding: 5px 0 !important;
                margin: 0 !important;
            }
            body:not(.print-single-tab) .crf-page:last-of-type {
                page-break-after: avoid !important;
                break-after: avoid !important;
            }

            /* Single Tab Mode: only print active form */
            body.print-single-tab .crf-page:not(.active) {
                display: none !important;
            }
            body.print-single-tab .crf-page.active {
                display: block !important;
                page-break-after: avoid !important;
                border: none !important;
                box-shadow: none !important;
                padding: 5px 0 !important;
            }

            .doc-header-box {
                padding: 6px 12px !important;
                margin-bottom: 6px !important;
                page-break-inside: avoid !important;
                break-inside: avoid !important;
            }
            .doc-header-box h2 {
                font-size: 14.5px !important;
                margin-bottom: 1px !important;
            }
            .doc-header-box h3 {
                font-size: 13px !important;
                margin-bottom: 1px !important;
            }
            .doc-header-box p {
                font-size: 11px !important;
            }

            .section-header {
                font-size: 13px !important;
                margin: 8px 0 4px 0 !important;
                padding: 2px 6px !important;
                page-break-inside: avoid !important;
                break-inside: avoid !important;
            }

            .crf-table {
                margin-bottom: 6px !important;
                font-size: 11.5px !important;
                page-break-inside: auto;
            }

            .crf-table tr {
                page-break-inside: avoid !important;
                break-inside: avoid !important;
            }

            .crf-table th, .crf-table td {
                padding: 3px 5px !important;
            }

            input[type="text"], input[type="number"], select, textarea, input[type="date"], input[type="time"] {
                border: none !important;
                border-bottom: 1px solid #94a3b8 !important;
                border-radius: 0 !important;
                background: transparent !important;
                font-weight: 600 !important;
                color: #0f172a !important;
                padding: 1px 3px !important;
                height: 22px !important;
                font-size: 11.5px !important;
                box-shadow: none !important;
                -webkit-appearance: none !important;
                -moz-appearance: none !important;
                appearance: none !important;
            }

            .input-calc {
                background: #f1f5f9 !important;
                border: 1px solid #cbd5e1 !important;
                font-weight: 700 !important;
            }

            .badge-calc, .badge-evaluated {
                padding: 1px 4px !important;
                font-size: 10px !important;
            }

            .form-check {
                font-size: 11.5px !important;
            }

            .form-check input[type="checkbox"], .form-check input[type="radio"] {
                width: 13px !important;
                height: 13px !important;
            }
        }
    """

print("get_css defined successfully")
