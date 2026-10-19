# -*- coding: utf-8 -*-
"""
Assembler script to build the complete index.html for Online CRF Web App (Forms 1, 2, 3, 4)
"""
import os
import sys

from generate_app import get_css
from build_form1 import get_form1_html
from build_form2 import get_form2_html
from build_form3 import get_form3_html
from build_form4 import get_form4_html
from build_admin_dashboard import get_admin_dashboard_html, get_admin_dashboard_css
from build_js import get_js

import re

OUTPUT_PATH = "/Users/nuttp./Desktop/MSc CU/Thesis/CRF/Online_CRF/index.html"

def wrap_tables(content):
    pattern = re.compile(r'(<table\b[^>]*class=[\'"][^\'"]*crf-table[^\'"]*[\'"][^>]*>[\s\S]*?</table>)', re.IGNORECASE)
    def repl(m):
        return f'<div class="table-responsive">{m.group(1)}</div>'
    return pattern.sub(repl, content)

def assemble():
    css_content = get_css()
    admin_css = get_admin_dashboard_css()
    admin_dashboard_html = get_admin_dashboard_html()
    f1_html = wrap_tables(get_form1_html())
    f2_html = wrap_tables(get_form2_html())
    f3_html = wrap_tables(get_form3_html())
    f4_html = wrap_tables(get_form4_html())
    js_content = get_js()

    html = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ระบบบันทึกข้อมูลการวิจัยทางคลินิกออนไลน์ (Clinical Research CRF)</title>
    <!-- Google Fonts: Sarabun -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <style>
{css_content}
{admin_css}
    </style>
</head>
<body>

    <!-- Sticky Top Navbar -->
    <header class="top-navbar">
        <div class="navbar-content">
            <div class="nav-title-group">
                <h1>ระบบบันทึกข้อมูลการวิจัยทางคลินิกออนไลน์ (Online Emergency Transfer CRF)</h1>
                <p title="Timeliness, delay determinants, and early clinical outcomes of emergency transfers from an island district hospital to a mainland referral hospital: a retrospective cohort study">โครงการวิจัย: ความทันเวลา ปัจจัยกำหนดความล่าช้า และผลลัพธ์ทางคลินิกระยะแรกของการส่งต่อผู้ป่วยฉุกเฉินจากโรงพยาบาลชุมชนบนเกาะสู่โรงพยาบาลรับส่งต่อบนแผ่นดินใหญ่: การศึกษาตามรุ่นย้อนหลัง</p>
            </div>
            <div class="nav-actions">
                <span id="save-status" class="save-status" style="display:none;">✓ บันทึกอัตโนมัติแล้ว</span>
                <select id="case-selector" onchange="onCaseSelected(this)" style="width: 170px; padding: 5px 8px; font-weight: 600; font-size: 13px;">
                    <option value="">-- เคสที่บันทึกไว้ --</option>
                </select>
                <button type="button" class="btn btn-success" onclick="createNewCase()" title="สร้างเคสผู้ป่วยใหม่">
                    ➕ เคสใหม่
                </button>
                <button type="button" class="btn btn-blue" onclick="saveCurrentCase(false)" title="บันทึกข้อมูลเคสปัจจุบัน">
                    💾 บันทึกเคส
                </button>
                <button type="button" class="btn btn-admin" onclick="openAdminDashboard()" title="เข้าสู่ระบบผู้ดูแลเพื่อดูสรุป ลบ หรือแก้ไขข้อมูลคนไข้ทั้งหมด">
                    🔐 Admin Dashboard
                </button>
                <div id="nav-user-container" style="display: flex; align-items: center; gap: 8px; margin-left: 6px; padding-left: 10px; border-left: 1.5px solid #cbd5e1; flex-shrink: 0;">
                    <div id="nav-user-info" style="display: none; align-items: center; gap: 6px; font-size: 13px; color: #1e293b; background: #f8fafc; border: 1px solid #cbd5e1; padding: 4px 10px; border-radius: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                        <span style="font-size: 14px;">👤</span>
                        <span id="nav-user-fullname" style="font-weight: 700; color: #0f172a; max-width: 160px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">-</span>
                        <span id="nav-user-badge" style="font-size: 10.5px; padding: 1.5px 7px; border-radius: 999px; background: #2563eb; color: #ffffff; font-weight: 700;">ผู้สกัดข้อมูล</span>
                    </div>
                    <button type="button" id="btn-login" class="btn btn-primary" onclick="openLoginModal()" style="font-size: 13px; padding: 5px 14px; background: #1e40af; color: #ffffff; border: 1px solid #1d4ed8; font-weight: 700; border-radius: 6px;" title="เข้าสู่ระบบเพื่อบันทึกข้อมูล">
                        🔑 เข้าสู่ระบบ
                    </button>
                    <button type="button" id="btn-logout" class="btn" onclick="logoutUser()" style="display: none; font-size: 12px; padding: 4px 10px; color: #b91c1c; border: 1px solid #fecdd3; background: #fff1f2; font-weight: 600; border-radius: 6px;" title="ออกจากระบบ">
                        🚪 ออกจากระบบ
                    </button>
                </div>
            </div>
        </div>
        <!-- Progress Bar Indicator -->
        <div style="height: 4px; background: #e2e8f0; width: 100%; margin-top: 10px; border-radius: 2px; overflow: hidden;">
            <div id="progress-bar" style="height: 100%; background: #1e40af; width: 25%; transition: all 0.3s ease;"></div>
        </div>
    </header>

    <!-- Tab Bar -->
    <div class="tab-bar-container">
        <nav class="tab-bar">
            <button type="button" id="tab-btn-1" class="tab-btn tab-form1 active" onclick="switchTab(1)">
                <span>ส่วนที่ 1: การคัดกรอง ข้อมูลประชากร และแรกรับ รพ.เกาะลันตา</span>
                <span class="tab-badge">Form 1</span>
            </button>
            <button type="button" id="tab-btn-2" class="tab-btn tab-form2" onclick="switchTab(2)">
                <span>ส่วนที่ 2: เส้นเวลาส่งต่อ การข้ามแพ และการบริบาลระหว่างทาง</span>
                <span class="tab-badge">Form 2</span>
            </button>
            <button type="button" id="tab-btn-3" class="tab-btn tab-form3" onclick="switchTab(3)">
                <span>ส่วนที่ 3: สภาพแวดล้อม อุทกศาสตร์ และอุตุนิยมวิทยา</span>
                <span class="tab-badge">Form 3</span>
            </button>
            <button type="button" id="tab-btn-4" class="tab-btn tab-form4" onclick="switchTab(4)">
                <span>ส่วนที่ 4: การรักษา สรีรวิทยาเปรียบเทียบ และผลลัพธ์ รพ.กระบี่</span>
                <span class="tab-badge">Form 4</span>
            </button>
        </nav>
    </div>

    <!-- Main Content Container -->
    <main class="main-container">
        <!-- Auth Lock Banner -->
        <div id="auth-locked-banner" style="display: none; background: #fff7ed; border: 2px dashed #f97316; border-radius: 8px; padding: 14px 18px; margin-bottom: 18px; text-align: center; box-shadow: 0 2px 8px rgba(249, 115, 22, 0.08);">
            <div style="font-size: 26px; margin-bottom: 4px;">🔒</div>
            <div style="font-size: 16px; font-weight: 800; color: #c2410c; margin-bottom: 4px;">
                ระบบอยู่ในสถานะล็อกการกรอกข้อมูล (Authentication Required)
            </div>
            <div style="font-size: 13.5px; color: #7c2d12; line-height: 1.5; margin-bottom: 10px;">
                คุณยังไม่ได้เข้าสู่ระบบ กรุณาเข้าสู่ระบบด้วยบัญชีผู้ใช้งานที่ได้รับอนุญาตเพื่อเริ่มบันทึก แก้ไข หรือจัดการข้อมูลผู้ป่วย<br>
                <span style="font-size: 12px; color: #9a3412;">(หากยังไม่มีบัญชีผู้ใช้งาน กรุณาติดต่อผู้ดูแลระบบ [Admin] เพื่อสร้างบัญชีใหม่)</span>
            </div>
            <button type="button" class="btn btn-blue" onclick="openLoginModal()" style="padding: 6px 18px; font-size: 13.5px; font-weight: 700;">
                🔑 เข้าสู่ระบบทันที (Sign In)
            </button>
        </div>

        <form id="crf-master-form" onsubmit="return false;">
{f1_html}
{f2_html}
{f3_html}
{f4_html}
        </form>
    </main>

    <!-- Bottom Navigation Bar -->
    <footer class="bottom-nav-bar">
        <div class="bottom-nav-content">
            <div>
                <button type="button" id="btn-nav-prev" class="btn btn-outline" onclick="prevTab();" style="visibility: hidden;">
                    ⬅ ย้อนกลับไปหน้าก่อนหน้า
                </button>
            </div>
            <div style="display: flex; gap: 10px; align-items: center;">
                <button type="button" id="btn-nav-next" class="btn btn-theme-2" onclick="nextTab();">
                    <span>ถัดไป: ส่วนที่ 2 (Form 2) ➔</span>
                </button>
            </div>
        </div>
    </footer>

    <!-- PDF Export Option Modal -->
    <div id="pdf-export-modal" class="modal-overlay" style="display:none;">
        <div class="modal-box" style="max-width: 440px;">
            <div class="modal-header" style="background: linear-gradient(135deg, #1e40af 0%, #0369a1 100%); color: #ffffff;">
                <h3 style="font-size: 16px; font-weight: 700; color: #ffffff; display: flex; align-items: center; gap: 8px;">
                    <span>📄 ส่งออกรายงานผู้ป่วยรายบุคคลเป็น PDF</span>
                </h3>
                <button type="button" class="modal-close-btn" onclick="closePdfModal()" style="color: #ffffff;">✕</button>
            </div>
            <div style="padding: 20px;">
                <div style="margin-bottom: 15px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px;">
                    <div style="font-size: 13px; color: #64748b; margin-bottom: 4px;">ข้อมูลเคสที่เลือกส่งออก:</div>
                    <div id="pdf-target-case-info" style="font-size: 15px; font-weight: 700; color: #1e40af;">
                        เคสปัจจุบัน (LANTA_001)
                    </div>
                </div>
                
                <p style="font-size: 13.5px; color: #475569; margin-bottom: 14px;">
                    เลือกรูปแบบรายงานที่ต้องการสั่งพิมพ์ หรือบันทึกเป็น PDF (Save as PDF):
                </p>

                <div style="display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px;">
                    <button type="button" class="btn btn-primary" onclick="executeExportPDF(true)" style="padding: 10px 14px; text-align: left; display: flex; flex-direction: column; gap: 3px;">
                        <span style="font-weight: 700; font-size: 14px;">📑 บันทึกทุกส่วนรวมกันเป็นเล่มเดียว (Forms 1 - 4 ครบชุด)</span>
                        <span style="font-size: 12px; opacity: 0.9; font-weight: 400;">จัดแบ่งหน้า A4 อัตโนมัติ ครบถ้วนตั้งแต่แรกรับเกาะลันตา เส้นทางข้ามแพ สภาพทะเล และรพ.กระบี่</span>
                    </button>
                    <button type="button" class="btn btn-outline" onclick="executeExportPDF(false)" style="padding: 10px 14px; text-align: left; display: flex; flex-direction: column; gap: 3px; border-color: #94a3b8;">
                        <span style="font-weight: 700; font-size: 14px; color: #0f172a;">📄 บันทึกเฉพาะหน้าที่เปิดอยู่ปัจจุบัน (Current Active Form)</span>
                        <span style="font-size: 12px; color: #64748b; font-weight: 400;">พิมพ์เฉพาะฟอร์มที่กำลังแสดงผลอยู่บนหน้าจอขณะนี้</span>
                    </button>
                </div>

                <div style="font-size: 12px; color: #64748b; background: #f1f5f9; padding: 8px 10px; border-radius: 6px; line-height: 1.4;">
                    💡 <b>คำแนะนำการบันทึก PDF:</b> เมื่อหน้าต่างพิมพ์ของเบราว์เซอร์ปรากฏขึ้น ในช่อง <i>Destination (เครื่องพิมพ์)</i> ให้เลือกเป็น <b>"Save as PDF"</b> หรือ <b>"บันทึกเป็น PDF"</b>
                </div>

                <div style="display: flex; justify-content: flex-end; margin-top: 15px;">
                    <button type="button" class="btn btn-outline" onclick="closePdfModal()">ปิด</button>
                </div>
            </div>
        </div>
    </div>

    <!-- User Login Modal -->
    <div id="user-login-modal" class="modal-overlay" style="display:none; z-index: 3000;">
        <div class="modal-box" style="max-width: 420px; border-radius: 10px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
            <div class="modal-header" style="background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%); color: #ffffff; padding: 14px 20px;">
                <h3 style="font-size: 16px; font-weight: 700; color: #ffffff; display: flex; align-items: center; gap: 8px; margin: 0;">
                    <span>🔐 เข้าสู่ระบบบันทึกข้อมูลวิจัย (CRF Login)</span>
                </h3>
                <button type="button" class="modal-close-btn" onclick="closeLoginModal()" style="color: #ffffff; font-size: 18px;">✕</button>
            </div>
            <div style="padding: 20px 24px; background: #ffffff;">
                <div id="login-modal-notice" style="font-size: 13px; color: #475569; margin-bottom: 14px; line-height: 1.5;">
                    กรุณากรอกชื่อผู้ใช้และรหัสผ่านเพื่อเริ่มบันทึกข้อมูล (ชื่อจริง-นามสกุลของคุณจะถูกบันทึกเป็นผู้สกัดข้อมูลอัตโนมัติ)
                </div>

                <div style="margin-bottom: 12px;">
                    <label style="display: block; font-size: 13px; font-weight: 700; color: #1e293b; margin-bottom: 4px;">
                        ชื่อผู้ใช้งาน (Username)
                    </label>
                    <input type="text" id="login-username" placeholder="กรอก Username" autocomplete="username"
                           style="width: 100%; font-size: 14px; padding: 8px 12px; border: 1.5px solid #cbd5e1; border-radius: 6px;"
                           onkeydown="if(event.key==='Enter') document.getElementById('login-password')?.focus();">
                </div>

                <div style="margin-bottom: 12px;">
                    <label style="display: block; font-size: 13px; font-weight: 700; color: #1e293b; margin-bottom: 4px;">
                        รหัสผ่าน (Password)
                    </label>
                    <input type="password" id="login-password" placeholder="กรอกรหัสผ่าน" autocomplete="current-password"
                           style="width: 100%; font-size: 14px; padding: 8px 12px; border: 1.5px solid #cbd5e1; border-radius: 6px;"
                           onkeydown="if(event.key==='Enter') submitUserLogin();">
                </div>

                <div id="login-error-msg" style="display: none; background: #fef2f2; border: 1px solid #fecaca; border-radius: 6px; padding: 8px 12px; color: #b91c1c; font-size: 12.5px; font-weight: 600; margin-bottom: 12px;">
                    ❌ ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง
                </div>

                <div style="display: flex; gap: 8px; justify-content: flex-end;">
                    <button type="button" class="btn btn-outline" onclick="closeLoginModal()">ยกเลิก</button>
                    <button type="button" class="btn btn-primary" onclick="submitUserLogin()" style="background: #1e40af; color: #ffffff; padding: 6px 18px; font-weight: 700;">
                        เข้าสู่ระบบ ➔
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Admin Authentication Modal -->
    <div id="admin-auth-modal" class="modal-overlay" style="display:none;">
        <div class="modal-box" style="max-width: 380px;">
            <div class="modal-header">
                <h3 style="font-size: 16px; font-weight: 700; color: #1e1b4b;">🔐 เข้าสู่ระบบ Admin</h3>
                <button type="button" class="modal-close-btn" onclick="closeAdminAuthModal()">✕</button>
            </div>
            <div style="padding: 20px; text-align: center;">
                <p style="font-size: 14px; color: #475569; margin-bottom: 15px;">
                    กรุณากรอกรหัสผ่านผู้ดูแลระบบ เพื่อดูสรุปคนไข้ทั้งหมด แก้ไข หรือลบข้อมูล
                </p>
                <div style="margin-bottom: 12px;">
                    <input type="password" id="admin-password-input" placeholder="กรอกรหัสผ่าน Admin" 
                           style="width: 100%; font-size: 18px; text-align: center; letter-spacing: 2px; padding: 6px 10px; border: 2px solid #cbd5e1; border-radius: 6px;"
                           onkeydown="if(event.key==='Enter') verifyAdminPassword();">
                </div>
                <div id="admin-auth-error" style="display: none; color: #b91c1c; font-size: 13px; font-weight: 700; margin-bottom: 12px;">
                    ❌ รหัสผ่านไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง
                </div>
                <div style="display: flex; gap: 8px; justify-content: center; margin-top: 15px;">
                    <button type="button" class="btn btn-outline" onclick="closeAdminAuthModal()">ยกเลิก</button>
                    <button type="button" class="btn btn-admin" onclick="verifyAdminPassword()">เข้าสู่ระบบ ➔</button>
                </div>
            </div>
        </div>
    </div>

{admin_dashboard_html}

    <!-- SheetJS for Offline Excel Export & Online CDN Fallback -->
    <script src="./xlsx.full.min.js"></script>
    <script>
        if (typeof XLSX === 'undefined') {{
            var s = document.createElement('script');
            s.src = 'https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js';
            document.head.appendChild(s);
        }}
    </script>

    <!-- Embedded Application Logic -->
    <script>
{js_content}
    </script>
</body>
</html>
"""
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    
    file_size = os.path.getsize(OUTPUT_PATH)
    print(f"Successfully generated {OUTPUT_PATH} ({file_size} bytes)")

if __name__ == "__main__":
    assemble()
