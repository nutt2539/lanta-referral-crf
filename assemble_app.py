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

    <!-- Admin Dashboard Modal -->
    <div id="admin-dashboard-modal" class="modal-overlay" style="display:none;">
        <div class="modal-box modal-box-large">
            <!-- Dashboard Header -->
            <div class="modal-header" style="background: linear-gradient(135deg, #1e1b4b 0%, #3b0764 100%); color: #ffffff; padding: 12px 20px; border-radius: 8px 8px 0 0;">
                <div>
                    <h2 style="font-size: 18px; font-weight: 700; display: flex; align-items: center; gap: 8px; color: #ffffff;">
                        <span>📊 แดชบอร์ดสรุปและจัดการข้อมูลผู้ป่วย (Admin Dashboard)</span>
                        <span style="font-size: 11px; background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 999px; font-weight: 500;">Authorized</span>
                    </h2>
                    <p style="font-size: 12.5px; opacity: 0.85; margin-top: 1px; color: #e2e8f0;">
                        ระบบฐานข้อมูลผู้ป่วยส่งต่อฉุกเฉินออนไลน์ รพ.เกาะลันตา - รพ.กระบี่
                    </p>
                </div>
                <div style="display: flex; gap: 8px; align-items: center;">
                    <button type="button" class="btn btn-success" onclick="exportToExcel()" style="font-size: 13px; padding: 4px 10px;" title="ดาวน์โหลดฐานข้อมูลทุกเคสเป็นไฟล์ Excel (.xlsx)">
                        📥 Export Excel
                    </button>
                    <button type="button" class="btn btn-blue" onclick="openPdfModal()" style="font-size: 13px; padding: 4px 10px;" title="ส่งออกรายงานข้อมูลคนไข้เป็น PDF หรือสั่งพิมพ์">
                        📄 Export PDF
                    </button>
                    <button type="button" class="btn btn-outline" onclick="adminLogout()" style="font-size: 13px; padding: 4px 10px; color: #fca5a5; border-color: rgba(255,255,255,0.3); background: transparent;" title="ออกจากระบบผู้ดูแล">
                        🔒 ล็อคระบบ
                    </button>
                    <button type="button" class="modal-close-btn" onclick="closeAdminDashboard()" style="color: #ffffff; font-size: 18px;" title="ปิดหน้าต่าง">✕</button>
                </div>
            </div>

            <!-- Dashboard Content -->
            <div style="padding: 16px 20px; background: #f8fafc; max-height: calc(85vh - 100px); overflow-y: auto;">
                <!-- Summary Stat Cards -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-bottom: 16px;">
                    <!-- Card 1: Total Patients -->
                    <div style="background: #ffffff; border: 1px solid #cbd5e1; border-left: 4px solid #1e40af; border-radius: 6px; padding: 10px 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                        <div style="font-size: 12.5px; color: #64748b; font-weight: 600;">ผู้ป่วยในฐานข้อมูลทั้งหมด</div>
                        <div id="stat-total-patients" style="font-size: 26px; font-weight: 700; color: #1e40af; line-height: 1.2; margin-top: 2px;">0</div>
                        <div style="font-size: 11.5px; color: #94a3b8;">เคสที่บันทึกแล้วในเบราว์เซอร์</div>
                    </div>
                    <!-- Card 2: Mean Transfer Time -->
                    <div style="background: #ffffff; border: 1px solid #cbd5e1; border-left: 4px solid #0f766e; border-radius: 6px; padding: 10px 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                        <div style="font-size: 12.5px; color: #64748b; font-weight: 600;">เวลาส่งต่อเฉลี่ย (T0 ➔ T10)</div>
                        <div id="stat-mean-time" style="font-size: 26px; font-weight: 700; color: #0f766e; line-height: 1.2; margin-top: 2px;">0 <span style="font-size: 14px; font-weight: 500;">นาที</span></div>
                        <div id="stat-time-detail" style="font-size: 11.5px; color: #94a3b8;">จากเคสที่มีข้อมูลเวลาครบ</div>
                    </div>
                    <!-- Card 3: ESI Level 1 -->
                    <div style="background: #ffffff; border: 1px solid #cbd5e1; border-left: 4px solid #b91c1c; border-radius: 6px; padding: 10px 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                        <div style="font-size: 12.5px; color: #64748b; font-weight: 600;">ผู้ป่วยวิกฤตฉุกเฉิน (ESI 1)</div>
                        <div id="stat-esi1-count" style="font-size: 26px; font-weight: 700; color: #b91c1c; line-height: 1.2; margin-top: 2px;">0</div>
                        <div id="stat-esi1-pct" style="font-size: 11.5px; color: #94a3b8;">0% ของผู้ป่วยทั้งหมด</div>
                    </div>
                    <!-- Card 4: Survival Rate -->
                    <div style="background: #ffffff; border: 1px solid #cbd5e1; border-left: 4px solid #16a34a; border-radius: 6px; padding: 10px 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                        <div style="font-size: 12.5px; color: #64748b; font-weight: 600;">อัตรารอดชีวิต 24 ชม. รพ.กระบี่</div>
                        <div id="stat-survival-rate" style="font-size: 26px; font-weight: 700; color: #16a34a; line-height: 1.2; margin-top: 2px;">100%</div>
                        <div id="stat-survival-detail" style="font-size: 11.5px; color: #94a3b8;">Early Survival Outcome</div>
                    </div>
                </div>

                <!-- Clinical Research Pie Charts Overview -->
                <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px 16px; margin-bottom: 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px;">
                        <div style="font-size: 14px; font-weight: 700; color: #1e3a8a; display: flex; align-items: center; gap: 6px;">
                            <span>📊 แผนภูมิวิเคราะห์สัดส่วนข้อมูลทางคลินิก (Clinical Research Distribution)</span>
                        </div>
                        <span style="font-size: 11.5px; color: #64748b; font-weight: 500;">สรุปสัดส่วนตัวแปรสำคัญจากฐานข้อมูลจริง</span>
                    </div>

                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px;">
                        <!-- Chart 1: Target Disease -->
                        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 12px;">
                            <div style="font-size: 12.5px; font-weight: 700; color: #1e293b; margin-bottom: 8px; display: flex; align-items: center; gap: 5px;">
                                <span>🫀 กลุ่มโรคเป้าหมาย (Disease)</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <div id="pie-chart-disease" style="width: 82px; height: 82px; border-radius: 50%; position: relative; flex-shrink: 0; box-shadow: 0 1px 4px rgba(0,0,0,0.08); background: #e2e8f0;">
                                    <div style="position: absolute; inset: 17px; background: #ffffff; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);">
                                        <span id="pie-center-disease" style="font-size: 13px; font-weight: 700; color: #1e293b; line-height: 1;">0</span>
                                        <span style="font-size: 8.5px; color: #64748b;">เคส</span>
                                    </div>
                                </div>
                                <div id="pie-legend-disease" style="flex: 1; min-width: 0;"></div>
                            </div>
                        </div>

                        <!-- Chart 2: Transfer Timeliness -->
                        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 12px;">
                            <div style="font-size: 12.5px; font-weight: 700; color: #1e293b; margin-bottom: 8px; display: flex; align-items: center; gap: 5px;">
                                <span>⏱️ ความทันเวลาส่งต่อ (≤ 3 ชม.)</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <div id="pie-chart-timeliness" style="width: 82px; height: 82px; border-radius: 50%; position: relative; flex-shrink: 0; box-shadow: 0 1px 4px rgba(0,0,0,0.08); background: #e2e8f0;">
                                    <div style="position: absolute; inset: 17px; background: #ffffff; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);">
                                        <span id="pie-center-timeliness" style="font-size: 13px; font-weight: 700; color: #059669; line-height: 1;">0%</span>
                                        <span style="font-size: 8.5px; color: #64748b;">ทันเวลา</span>
                                    </div>
                                </div>
                                <div id="pie-legend-timeliness" style="flex: 1; min-width: 0;"></div>
                            </div>
                        </div>

                        <!-- Chart 3: Survival Outcome -->
                        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 12px;">
                            <div style="font-size: 12.5px; font-weight: 700; color: #1e293b; margin-bottom: 8px; display: flex; align-items: center; gap: 5px;">
                                <span>🏥 ผลลัพธ์รอดชีวิต 24 ชม.</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <div id="pie-chart-survival" style="width: 82px; height: 82px; border-radius: 50%; position: relative; flex-shrink: 0; box-shadow: 0 1px 4px rgba(0,0,0,0.08); background: #e2e8f0;">
                                    <div style="position: absolute; inset: 17px; background: #ffffff; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);">
                                        <span id="pie-center-survival" style="font-size: 13px; font-weight: 700; color: #16a34a; line-height: 1;">0%</span>
                                        <span style="font-size: 8.5px; color: #64748b;">รอดชีวิต</span>
                                    </div>
                                </div>
                                <div id="pie-legend-survival" style="flex: 1; min-width: 0;"></div>
                            </div>
                        </div>

                        <!-- Chart 4: Triage ESI -->
                        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 12px;">
                            <div style="font-size: 12.5px; font-weight: 700; color: #1e293b; margin-bottom: 8px; display: flex; align-items: center; gap: 5px;">
                                <span>🚨 ระดับความเร่งด่วน (ESI)</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <div id="pie-chart-esi" style="width: 82px; height: 82px; border-radius: 50%; position: relative; flex-shrink: 0; box-shadow: 0 1px 4px rgba(0,0,0,0.08); background: #e2e8f0;">
                                    <div style="position: absolute; inset: 17px; background: #ffffff; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);">
                                        <span id="pie-center-esi" style="font-size: 13px; font-weight: 700; color: #1e293b; line-height: 1;">0</span>
                                        <span style="font-size: 8.5px; color: #64748b;">เคส</span>
                                    </div>
                                </div>
                                <div id="pie-legend-esi" style="flex: 1; min-width: 0;"></div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Controls Toolbar -->
                <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 10px 14px; margin-bottom: 12px; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 10px;">
                    <div style="display: flex; gap: 8px; align-items: center; flex: 1; min-width: 260px;">
                        <span style="font-weight: 600; font-size: 13.5px;">🔍 ค้นหา:</span>
                        <input type="text" id="admin-search-box" oninput="filterAdminCases()" placeholder="พิมพ์ค้นหา STUDY_ID, HN, หรือเลขใบ Refer..." style="padding: 4px 8px; font-size: 13.5px; border: 1px solid #cbd5e1; border-radius: 4px; flex: 1;">
                    </div>
                    <div style="display: flex; gap: 8px; align-items: center;">
                        <span style="font-weight: 600; font-size: 13.5px;">กรอง ESI:</span>
                        <select id="admin-esi-filter" onchange="filterAdminCases()" style="padding: 4px 8px; font-size: 13.5px; border: 1px solid #cbd5e1; border-radius: 4px; width: 130px;">
                            <option value="">ทั้งหมด (All)</option>
                            <option value="1">ESI 1 (Resuscitation)</option>
                            <option value="2">ESI 2 (Emergent)</option>
                            <option value="3">ESI 3 (Urgent)</option>
                            <option value="4">ESI 4 (Semi-urgent)</option>
                            <option value="5">ESI 5 (Non-urgent)</option>
                        </select>
                        <button type="button" class="btn btn-primary" onclick="createNewCase(); closeAdminDashboard();" style="font-size: 13px; padding: 5px 12px;">
                            ➕ เคสใหม่
                        </button>
                    </div>
                </div>

                <!-- Patient Cases Table -->
                <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                    <div class="table-responsive" style="margin-bottom: 0;">
                        <table class="crf-table" style="margin-bottom: 0; font-size: 13px; width: 100%;">
                            <thead>
                                <tr style="background: #f1f5f9;">
                                    <th style="width: 100px; text-align: center;">STUDY_ID</th>
                                    <th style="width: 130px;">HN / Refer_ID</th>
                                    <th style="width: 100px; text-align: center;">อายุ / เพศ</th>
                                    <th style="width: 90px; text-align: center;">Triage ESI</th>
                                    <th>หมวดโรค / การวินิจฉัย</th>
                                    <th style="width: 130px; text-align: center;">เวลาส่งต่อรวม</th>
                                    <th style="width: 90px; text-align: center;">RTS (เกาะ/กระบี่)</th>
                                    <th style="width: 100px; text-align: center;">ผลลัพธ์ 24 ชม.</th>
                                    <th style="width: 200px; text-align: center;">จัดการข้อมูล</th>
                                </tr>
                            </thead>
                            <tbody id="admin-cases-tbody">
                                <!-- Populated dynamically by JS -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Modal Footer -->
            <div style="padding: 10px 18px; background: #ffffff; border-top: 1px solid #cbd5e1; border-radius: 0 0 8px 8px; display: flex; justify-content: space-between; align-items: center;">
                <div style="font-size: 12.5px; color: #64748b;">
                    💡 คลิก <b>"ดู/แก้ไข"</b> เพื่อเปิดดูหรือแก้ไขข้อมูลในฟอร์ม หรือคลิก <b>"ลบ"</b> หากต้องการถอนเคสออกจากฐานข้อมูล
                </div>
                <button type="button" class="btn btn-outline" onclick="closeAdminDashboard()" style="padding: 4px 12px; font-size: 13px;">
                    ปิดหน้าต่าง
                </button>
            </div>
        </div>
    </div>

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
