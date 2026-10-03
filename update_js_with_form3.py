# -*- coding: utf-8 -*-
"""
Script to rewrite build_js.py with complete support for Form 1, Form 2, Form 3, and Form 4
"""

js_code = r'''# -*- coding: utf-8 -*-
"""
JavaScript Engine Generator module for Online CRF (Forms 1, 2, 3, 4)
"""

def get_js():
    return """
    // --- Online CRF JavaScript Engine ---

    // Global Active Tab State (1: Form 1, 2: Form 2, 3: Form 3, 4: Form 4)
    let currentTab = 1;

    // Initialize on DOM load
    document.addEventListener('DOMContentLoaded', function() {
        initSyncFields();
        initAutoSave();
        loadCaseIndex();
        
        // Load latest case or default
        const lastCaseId = localStorage.getItem('online_crf_last_active_id');
        if (lastCaseId) {
            loadCase(lastCaseId);
        } else {
            document.getElementById('f1_study_id').value = '001';
            syncFields('study-id-sync', '001');
            calcAll();
        }
    });

    // --- Tab Navigation ---
    function switchTab(tabIndex) {
        currentTab = Number(tabIndex);
        document.querySelectorAll('.crf-page').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));

        const targetPage = document.getElementById('page-form' + currentTab);
        const targetBtn = document.getElementById('tab-btn-' + currentTab);
        if (targetPage) targetPage.classList.add('active');
        if (targetBtn) targetBtn.classList.add('active');

        // Update progress indicator
        const progressEl = document.getElementById('progress-bar');
        if (progressEl) {
            if (currentTab === 1) progressEl.style.width = '25%';
            else if (currentTab === 2) progressEl.style.width = '50%';
            else if (currentTab === 3) progressEl.style.width = '75%';
            else if (currentTab === 4) progressEl.style.width = '100%';
        }

        updateBottomNav();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function updateBottomNav() {
        const prevBtn = document.getElementById('btn-nav-prev');
        const nextBtn = document.getElementById('btn-nav-next');
        if (!prevBtn || !nextBtn) return;

        if (currentTab === 1) {
            prevBtn.style.visibility = 'hidden';
            nextBtn.className = 'btn btn-primary';
            nextBtn.innerHTML = '<span>ถัดไป: ส่วนที่ 2 (Form 2) ➔</span>';
        } else if (currentTab === 2) {
            prevBtn.style.visibility = 'visible';
            prevBtn.innerHTML = '⬅ ย้อนกลับไปส่วนที่ 1 (Form 1)';
            nextBtn.className = 'btn btn-primary';
            nextBtn.innerHTML = '<span>ถัดไป: ส่วนที่ 3 (Form 3) ➔</span>';
        } else if (currentTab === 3) {
            prevBtn.style.visibility = 'visible';
            prevBtn.innerHTML = '⬅ ย้อนกลับไปส่วนที่ 2 (Form 2)';
            nextBtn.className = 'btn btn-primary';
            nextBtn.innerHTML = '<span>ถัดไป: ส่วนที่ 4 (Form 4) ➔</span>';
        } else if (currentTab === 4) {
            prevBtn.style.visibility = 'visible';
            prevBtn.innerHTML = '⬅ ย้อนกลับไปส่วนที่ 3 (Form 3)';
            nextBtn.className = 'btn btn-success';
            nextBtn.innerHTML = '<span>💾 บันทึกและ Export เป็น Excel (.xlsx) 📥</span>';
        }
    }

    function nextTab() {
        if (currentTab === 1) switchTab(2);
        else if (currentTab === 2) switchTab(3);
        else if (currentTab === 3) switchTab(4);
        else if (currentTab === 4) exportToExcel();
    }

    function prevTab() {
        if (currentTab === 4) switchTab(3);
        else if (currentTab === 3) switchTab(2);
        else if (currentTab === 2) switchTab(1);
    }

    // --- Synchronize Identifiers across Form 1, 2, 3, 4 ---
    function initSyncFields() {
        const syncMap = [
            { class: 'study-id-sync', name: 'STUDY_ID' },
            { class: 'refer-id-sync', name: 'Refer_ID' },
            { class: 'hn-sync', name: 'HN' },
            { class: 'vn-sync', name: 'VN' },
            { class: 'date-sync', name: 'Date' },
            { class: 'abs-sync', name: 'Abstractor' }
        ];

        syncMap.forEach(item => {
            const inputs = document.querySelectorAll('.' + item.class);
            inputs.forEach(input => {
                input.addEventListener('input', function() {
                    const val = this.value;
                    inputs.forEach(target => {
                        if (target !== input) target.value = val;
                    });
                    scheduleAutoSave();
                });
            });
        });
    }

    function syncFields(className, val) {
        document.querySelectorAll('.' + className).forEach(el => el.value = val);
    }

    function syncDiseaseGroup() {
        const stemi = document.getElementById('f1_inc4_stemi')?.checked;
        const ais = document.getElementById('f1_inc4_ais')?.checked;
        const trauma = document.getElementById('f1_inc4_trauma')?.checked;
        
        const inc4RadioYes = document.querySelector('input[name="f1_inc4"][value="yes"]');
        if (stemi || ais || trauma) {
            if (inc4RadioYes) inc4RadioYes.checked = true;
        }
        calcScreening();
        calcTimelines();
    }

    // --- Synchronize Timestamps between forms ---
    function syncT0() {
        const d = document.getElementById('f1_t0_date')?.value;
        const t = document.getElementById('f1_t0_time')?.value;
        const f2_d = document.getElementById('f2_t0_date');
        const f2_t = document.getElementById('f2_t0_time');
        if (f2_d) f2_d.value = d;
        if (f2_t) f2_t.value = t;
    }

    function syncT0_fromF2() {
        const d = document.getElementById('f2_t0_date')?.value;
        const t = document.getElementById('f2_t0_time')?.value;
        const f1_d = document.getElementById('f1_t0_date');
        const f1_t = document.getElementById('f1_t0_time');
        if (f1_d) f1_d.value = d;
        if (f1_t) f1_t.value = t;
    }

    function syncT1() {
        const d = document.getElementById('f1_t1_date')?.value;
        const t = document.getElementById('f1_t1_time')?.value;
        const f2_d = document.getElementById('f2_t1_date');
        const f2_t = document.getElementById('f2_t1_time');
        if (f2_d) f2_d.value = d;
        if (f2_t) f2_t.value = t;
    }

    function syncT1_fromF2() {
        const d = document.getElementById('f2_t1_date')?.value;
        const t = document.getElementById('f2_t1_time')?.value;
        const f1_d = document.getElementById('f1_t1_date');
        const f1_t = document.getElementById('f1_t1_time');
        if (f1_d) f1_d.value = d;
        if (f1_t) f1_t.value = t;
    }

    function syncT4() {
        const d = document.getElementById('f2_t4_date')?.value;
        const t = document.getElementById('f2_t4_time')?.value;
        const f4_d = document.getElementById('f4_t4_date');
        const f4_t = document.getElementById('f4_t4_time');
        if (f4_d) f4_d.value = d;
        if (f4_t) f4_t.value = t;
    }

    function syncT4_fromF4() {
        const d = document.getElementById('f4_t4_date')?.value;
        const t = document.getElementById('f4_t4_time')?.value;
        const f2_d = document.getElementById('f2_t4_date');
        const f2_t = document.getElementById('f2_t4_time');
        if (f2_d) f2_d.value = d;
        if (f2_t) f2_t.value = t;
    }

    function syncT5() {
        const d = document.getElementById('f2_t5_date')?.value;
        const t = document.getElementById('f2_t5_time')?.value;
        const f4_d = document.getElementById('f4_t5_date');
        const f4_t = document.getElementById('f4_t5_time');
        if (f4_d) f4_d.value = d;
        if (f4_t) f4_t.value = t;
    }

    function syncT5_fromF4() {
        const d = document.getElementById('f4_t5_date')?.value;
        const t = document.getElementById('f4_t5_time')?.value;
        const f2_d = document.getElementById('f2_t5_date');
        const f2_t = document.getElementById('f2_t5_time');
        if (f2_d) f2_d.value = d;
        if (f2_t) f2_t.value = t;
    }

    // --- Date/Time Parsing & Diff (in Minutes) ---
    function parseDateTime(dateStr, timeStr) {
        if (!timeStr) return null;
        if (!dateStr) dateStr = '2026-01-01'; // Default fallback date for intra-day
        return new Date(dateStr + 'T' + timeStr + ':00');
    }

    function diffMinutes(d1, t1, d2, t2) {
        if (!t1 || !t2) return null;
        let dt1 = parseDateTime(d1, t1);
        let dt2 = parseDateTime(d2, t2);
        if (!dt1 || !dt2) return null;
        
        // Midnight crossover handler
        if (dt2 < dt1 && d1 === d2) {
            dt2 = new Date(dt2.getTime() + 24 * 60 * 60 * 1000);
        }
        
        let diffMs = dt2.getTime() - dt1.getTime();
        return Math.round(diffMs / 60000);
    }

    // --- FORM 1 CALCULATIONS ---
    function calcScreening() {
        const inc1 = document.querySelector('input[name="f1_inc1"]:checked')?.value;
        const inc2 = document.querySelector('input[name="f1_inc2"]:checked')?.value;
        const inc3 = document.querySelector('input[name="f1_inc3"]:checked')?.value;
        const inc4 = document.querySelector('input[name="f1_inc4"]:checked')?.value;

        const exc1 = document.querySelector('input[name="f1_exc1"]:checked')?.value;
        const exc2 = document.querySelector('input[name="f1_exc2"]:checked')?.value;
        const exc3 = document.querySelector('input[name="f1_exc3"]:checked')?.value;
        const exc4 = document.querySelector('input[name="f1_exc4"]:checked')?.value;
        const exc5 = document.querySelector('input[name="f1_exc5"]:checked')?.value;

        const isIncAllYes = (inc1 === 'yes' && inc2 === 'yes' && inc3 === 'yes' && inc4 === 'yes');
        const isExcAnyYes = (exc1 === 'yes' || exc2 === 'yes' || exc3 === 'yes' || exc4 === 'yes' || exc5 === 'yes');

        const badge = document.getElementById('screening_badge');
        if (badge) badge.style.display = 'inline-block';

        if (isIncAllYes && !isExcAnyYes && exc1 && exc2 && exc3 && exc4 && exc5) {
            document.getElementById('f1_eligible_yes').checked = true;
            if (badge) {
                badge.className = 'badge-calc badge-ontime';
                badge.textContent = '✓ ผ่านเกณฑ์การวิจัย';
            }
        } else if (inc1 === 'no' || inc2 === 'no' || inc3 === 'no' || inc4 === 'no' || isExcAnyYes) {
            document.getElementById('f1_eligible_no').checked = true;
            if (badge) {
                badge.className = 'badge-calc badge-delay';
                badge.textContent = '✗ ไม่ผ่านเกณฑ์ (คัดออก)';
            }
        }
        scheduleAutoSave();
    }

    function toggleCciDm() {
        const chk = document.getElementById('f1_cci_dm_chk')?.checked;
        const rad1 = document.querySelector('input[name="f1_cci_dm_type"][value="1"]');
        if (chk && !document.querySelector('input[name="f1_cci_dm_type"]:checked')) {
            if (rad1) rad1.checked = true;
        } else if (!chk) {
            document.querySelectorAll('input[name="f1_cci_dm_type"]').forEach(r => r.checked = false);
        }
    }

    function toggleCciLiver() {
        const chk = document.getElementById('f1_cci_liver_chk')?.checked;
        const rad1 = document.querySelector('input[name="f1_cci_liver_type"][value="1"]');
        if (chk && !document.querySelector('input[name="f1_cci_liver_type"]:checked')) {
            if (rad1) rad1.checked = true;
        } else if (!chk) {
            document.querySelectorAll('input[name="f1_cci_liver_type"]').forEach(r => r.checked = false);
        }
    }

    function toggleCciTumor() {
        const chk = document.getElementById('f1_cci_tumor_chk')?.checked;
        const rad2 = document.querySelector('input[name="f1_cci_tumor_type"][value="2"]');
        if (chk && !document.querySelector('input[name="f1_cci_tumor_type"]:checked')) {
            if (rad2) rad2.checked = true;
        } else if (!chk) {
            document.querySelectorAll('input[name="f1_cci_tumor_type"]').forEach(r => r.checked = false);
        }
    }

    function calcCCI() {
        const ageVal = parseInt(document.getElementById('f1_age')?.value, 10);
        let agePoints = 0;
        if (!isNaN(ageVal)) {
            if (ageVal < 50) agePoints = 0;
            else if (ageVal <= 59) agePoints = 1;
            else if (ageVal <= 69) agePoints = 2;
            else if (ageVal <= 79) agePoints = 3;
            else if (ageVal >= 80) agePoints = 4;
        }

        const badge = document.getElementById('f1_age_score_badge');
        if (badge) badge.textContent = '+' + agePoints + ' คะแนน';

        let comorbPoints = 0;

        // DM
        if (document.getElementById('f1_cci_dm_chk')?.checked) {
            const dmType = document.querySelector('input[name="f1_cci_dm_type"]:checked')?.value;
            comorbPoints += (dmType === '2') ? 2 : 1;
        }
        // Liver
        if (document.getElementById('f1_cci_liver_chk')?.checked) {
            const livType = document.querySelector('input[name="f1_cci_liver_type"]:checked')?.value;
            comorbPoints += (livType === '3') ? 3 : 1;
        }
        // Tumor
        if (document.getElementById('f1_cci_tumor_chk')?.checked) {
            const tumType = document.querySelector('input[name="f1_cci_tumor_type"]:checked')?.value;
            comorbPoints += (tumType === '6') ? 6 : 2;
        }

        // Single Checkboxes (+1)
        if (document.getElementById('f1_cci_mi')?.checked) comorbPoints += 1;
        if (document.getElementById('f1_cci_chf')?.checked) comorbPoints += 1;
        if (document.getElementById('f1_cci_pvd')?.checked) comorbPoints += 1;
        if (document.getElementById('f1_cci_stroke')?.checked) comorbPoints += 1;
        if (document.getElementById('f1_cci_dementia')?.checked) comorbPoints += 1;
        if (document.getElementById('f1_cci_copd')?.checked) comorbPoints += 1;
        if (document.getElementById('f1_cci_ctd')?.checked) comorbPoints += 1;
        if (document.getElementById('f1_cci_pud')?.checked) comorbPoints += 1;

        // Single Checkboxes (+2)
        if (document.getElementById('f1_cci_hemi')?.checked) comorbPoints += 2;
        if (document.getElementById('f1_cci_ckd')?.checked) comorbPoints += 2;
        if (document.getElementById('f1_cci_leukemia')?.checked) comorbPoints += 2;
        if (document.getElementById('f1_cci_lymphoma')?.checked) comorbPoints += 2;

        // Single Checkboxes (+6)
        if (document.getElementById('f1_cci_aids')?.checked) comorbPoints += 6;

        const totalCCI = comorbPoints + agePoints;
        const totalEl = document.getElementById('f1_cci_total');
        if (totalEl) totalEl.value = totalCCI;

        const cPointEl = document.getElementById('f1_cci_comorb_points');
        if (cPointEl) cPointEl.textContent = comorbPoints;
        const aPointEl = document.getElementById('f1_cci_age_points');
        if (aPointEl) aPointEl.textContent = agePoints;

        scheduleAutoSave();
    }

    function calcVitals() {
        const sbp = parseFloat(document.getElementById('f1_sbp')?.value);
        const dbp = parseFloat(document.getElementById('f1_dbp')?.value);
        const hr = parseFloat(document.getElementById('f1_hr')?.value);

        let map = null;
        if (!isNaN(sbp) && !isNaN(dbp)) {
            map = Math.round(((sbp + 2 * dbp) / 3) * 10) / 10;
            document.getElementById('f1_map').value = map;
        } else {
            document.getElementById('f1_map').value = '';
        }

        if (map && !isNaN(hr)) {
            const msi = Math.round((hr / map) * 100) / 100;
            document.getElementById('f1_msi').value = msi.toFixed(2);
        } else {
            document.getElementById('f1_msi').value = '';
        }

        calcRTS();
        calcDeltaVitals();
        scheduleAutoSave();
    }

    function calcGCS() {
        const e = parseInt(document.getElementById('f1_gcs_e')?.value, 10);
        const v = parseInt(document.getElementById('f1_gcs_v')?.value, 10);
        const m = parseInt(document.getElementById('f1_gcs_m')?.value, 10);

        if (!isNaN(e) && !isNaN(v) && !isNaN(m)) {
            const total = e + v + m;
            document.getElementById('f1_gcs_total').value = total;

            // Auto-check Stroke Consciousness
            if (total >= 3 && total <= 8) {
                const r1 = document.getElementById('f1_stroke_gcs_1');
                if (r1) r1.checked = true;
            } else if (total >= 9 && total <= 12) {
                const r2 = document.getElementById('f1_stroke_gcs_2');
                if (r2) r2.checked = true;
            } else if (total >= 13 && total <= 15) {
                const r3 = document.getElementById('f1_stroke_gcs_3');
                if (r3) r3.checked = true;
            }
        } else {
            document.getElementById('f1_gcs_total').value = '';
        }

        calcRTS();
        calcDeltaGCS();
        scheduleAutoSave();
    }

    function calcRTS() {
        const gcs = parseInt(document.getElementById('f1_gcs_total')?.value, 10);
        const sbp = parseFloat(document.getElementById('f1_sbp')?.value);
        const rr = parseFloat(document.getElementById('f1_rr')?.value);

        if (isNaN(gcs) || isNaN(sbp) || isNaN(rr)) {
            document.getElementById('f1_rts_total').value = '';
            return;
        }

        let cGCS = (gcs >= 13) ? 4 : (gcs >= 9 ? 3 : (gcs >= 6 ? 2 : (gcs >= 4 ? 1 : 0)));
        let cSBP = (sbp > 89) ? 4 : (sbp >= 76 ? 3 : (sbp >= 50 ? 2 : (sbp >= 1 ? 1 : 0)));
        let cRR = (rr >= 10 && rr <= 29) ? 4 : (rr > 29 ? 3 : (rr >= 6 ? 2 : (rr >= 1 ? 1 : 0)));

        const rts = Math.round((0.9368 * cGCS + 0.7326 * cSBP + 0.2908 * cRR) * 1000) / 1000;
        document.getElementById('f1_rts_total').value = rts.toFixed(3);

        if (rts <= 6.0) {
            const crit = document.getElementById('f1_trauma_acuity_crit');
            if (crit) crit.checked = true;
        } else {
            const mod = document.getElementById('f1_trauma_acuity_mod');
            if (mod) mod.checked = true;
        }

        calcDeltaRTS();
        scheduleAutoSave();
    }

    function calcTimelines() {
        // Form 1 Onset to ER
        const oDate = document.getElementById('f1_onset_date')?.value;
        const oTime = document.getElementById('f1_onset_time')?.value;
        const t0Date = document.getElementById('f1_t0_date')?.value;
        const t0Time = document.getElementById('f1_t0_time')?.value;

        if (oTime && t0Time) {
            const diff = diffMinutes(oDate, oTime, t0Date, t0Time);
            if (diff !== null) {
                document.getElementById('f1_onset_to_er').value = diff;
            }
        }

        // Form 1 DIDO (T0 to T1)
        const t1Date = document.getElementById('f1_t1_date')?.value;
        const t1Time = document.getElementById('f1_t1_time')?.value;

        if (t0Time && t1Time) {
            const dido = diffMinutes(t0Date, t0Time, t1Date, t1Time);
            if (dido !== null) {
                document.getElementById('f1_dido_min').value = dido;
                document.getElementById('f2_t0_1_min').value = dido;

                const isTrauma = document.getElementById('f1_inc4_trauma')?.checked;
                const limit = isTrauma ? 60 : 45;

                if (dido <= limit) {
                    document.getElementById('f1_dido_ontime').checked = true;
                    document.getElementById('f2_dido_ontime').checked = true;
                } else {
                    document.getElementById('f1_dido_delay').checked = true;
                    document.getElementById('f2_dido_delay').checked = true;
                }
            }
        }

        calcForm2Timelines();
        calcForm3();
        calcForm4Timelines();
        scheduleAutoSave();
    }

    // --- FORM 2 CALCULATIONS ---
    function calcForm2Timelines() {
        const t0Date = document.getElementById('f2_t0_date')?.value;
        const t0Time = document.getElementById('f2_t0_time')?.value;
        const t1Date = document.getElementById('f2_t1_date')?.value;
        const t1Time = document.getElementById('f2_t1_time')?.value;
        const t2Date = document.getElementById('f2_t2_date')?.value;
        const t2Time = document.getElementById('f2_t2_time')?.value;
        const t3EmbarkDate = document.getElementById('f2_t3_embark_date')?.value;
        const t3EmbarkTime = document.getElementById('f2_t3_embark_time')?.value;
        const t3DisembarkDate = document.getElementById('f2_t3_disembark_date')?.value;
        const t3DisembarkTime = document.getElementById('f2_t3_disembark_time')?.value;
        const t4Date = document.getElementById('f2_t4_date')?.value;
        const t4Time = document.getElementById('f2_t4_time')?.value;
        const t5Date = document.getElementById('f2_t5_date')?.value;
        const t5Time = document.getElementById('f2_t5_time')?.value;

        // Auto sync T3 to Form 3
        if (t3EmbarkDate && document.getElementById('f3_t3_date')) {
            document.getElementById('f3_t3_date').value = t3EmbarkDate;
        }
        if (t3EmbarkTime && document.getElementById('f3_t3_time')) {
            document.getElementById('f3_t3_time').value = t3EmbarkTime;
        }

        const isTrauma = document.getElementById('f1_inc4_trauma')?.checked;
        const isStroke = document.getElementById('f1_inc4_ais')?.checked;

        // T0-1 Island DIDO
        if (t0Time && t1Time) {
            const dido = diffMinutes(t0Date, t0Time, t1Date, t1Time);
            if (dido !== null) {
                document.getElementById('f2_t0_1_min').value = dido;
                const limit = isTrauma ? 60 : 45;
                if (dido <= limit) document.getElementById('f2_dido_ontime').checked = true;
                else document.getElementById('f2_dido_delay').checked = true;
            }
        }

        // T2 Island Road (T1 to T2)
        if (t1Time && t2Time) {
            const road = diffMinutes(t1Date, t1Time, t2Date, t2Time);
            if (road !== null) {
                document.getElementById('f2_t2_min').value = road;
                if (road <= 12) document.getElementById('f2_road_ontime').checked = true;
                else document.getElementById('f2_road_delay').checked = true;
            }
        }

        // Waiting at Pier (T2 to T3 embark)
        if (t2Time && t3EmbarkTime) {
            const wait = diffMinutes(t2Date, t2Time, t3EmbarkDate, t3EmbarkTime);
            if (wait !== null) {
                document.getElementById('f2_t_wait_min').value = wait;
                if (wait <= 5) document.getElementById('f2_wait_ontime').checked = true;
                else document.getElementById('f2_wait_delay').checked = true;
            }
        }

        // T3 Water Crossing
        if (t3DisembarkTime) {
            const startT = t3EmbarkTime || t2Time;
            const startD = t3EmbarkTime ? t3EmbarkDate : t2Date;
            const water = diffMinutes(startD, startT, t3DisembarkDate, t3DisembarkTime);
            if (water !== null) {
                document.getElementById('f2_t3_min').value = water;
                if (water <= 24) document.getElementById('f2_water_ontime').checked = true;
                else document.getElementById('f2_water_delay').checked = true;
            }
        }

        // T4 Mainland Highway
        if (t3DisembarkTime && t4Time) {
            const hwy = diffMinutes(t3DisembarkDate, t3DisembarkTime, t4Date, t4Time);
            if (hwy !== null) {
                document.getElementById('f2_t4_min').value = hwy;
                if (hwy <= 60) document.getElementById('f2_hwy_ontime').checked = true;
                else document.getElementById('f2_hwy_delay').checked = true;
            }
        }

        // T_Total System Time
        if (t0Time && t4Time) {
            const total = diffMinutes(t0Date, t0Time, t4Date, t4Time);
            if (total !== null) {
                document.getElementById('f2_t_total_min').value = total;
                const totalLimit = isTrauma ? 156 : 141;
                if (total <= totalLimit) document.getElementById('f2_total_ontime').checked = true;
                else document.getElementById('f2_total_delay').checked = true;
            }
        }

        // T5 Definitive Management
        if (t0Time && t5Time) {
            const t5 = diffMinutes(t0Date, t0Time, t5Date, t5Time);
            if (t5 !== null) {
                document.getElementById('f2_t5_min').value = t5;
                const t5Limit = isStroke ? 156 : 180;
                if (t5 <= t5Limit) document.getElementById('f2_t5_ontime').checked = true;
                else document.getElementById('f2_t5_delay').checked = true;
            }
        }

        calcForm3();
        scheduleAutoSave();
    }

    function calcCompositeAE() {
        const cpr = document.querySelector('input[name="f2_ae_cpr"]:checked')?.value === '1';
        const intub = document.querySelector('input[name="f2_ae_intub"]:checked')?.value === '1';
        const inotropes = document.querySelector('input[name="f2_ae_inotropes"]:checked')?.value === '1';
        const dislodge = document.querySelector('input[name="f2_ae_dislodge"]:checked')?.value === '1';
        const death = document.querySelector('input[name="f2_ae_death"]:checked')?.value === '1';

        const isEvent = (cpr || intub || inotropes || dislodge || death);
        if (isEvent) {
            document.getElementById('f2_comp_event').checked = true;
        } else {
            document.getElementById('f2_comp_stable').checked = true;
        }

        calcCompositeDeterioration();
        scheduleAutoSave();
    }

    // --- FORM 3 CALCULATIONS ---
    function calcTide() {
        const h = parseFloat(document.getElementById('f3_tide_height')?.value);
        if (!isNaN(h)) {
            if (h < 1.0) {
                const low = document.getElementById('f3_tide_low');
                if (low) low.checked = true;
            } else {
                const norm = document.getElementById('f3_tide_normal');
                if (norm) norm.checked = true;
            }
        }
        scheduleAutoSave();
    }

    function calcRain() {
        const r = parseFloat(document.getElementById('f3_rainfall_mm')?.value);
        if (!isNaN(r)) {
            if (r >= 10.0) {
                const heavy = document.getElementById('f3_rain_heavy');
                if (heavy) heavy.checked = true;
            } else {
                const norm = document.getElementById('f3_rain_normal');
                if (norm) norm.checked = true;
            }
        }
        scheduleAutoSave();
    }

    function calcForm3() {
        // Season auto-evaluation
        const t3Date = document.getElementById('f3_t3_date')?.value || document.getElementById('f2_t3_embark_date')?.value || document.getElementById('f1_t0_date')?.value;
        if (t3Date) {
            const parts = t3Date.split('-');
            if (parts.length >= 2) {
                const m = parseInt(parts[1], 10);
                if (m >= 5 && m <= 10) {
                    const mon = document.getElementById('f3_season_monsoon');
                    if (mon) mon.checked = true;
                } else if (m >= 1 && m <= 12) {
                    const dry = document.getElementById('f3_season_dry');
                    if (dry) dry.checked = true;
                }
            }
        }

        // Sync ED shift from Form 1
        const f1Shift = document.querySelector('input[name="f1_shift"]:checked')?.value;
        if (f1Shift) {
            const shiftRad = document.querySelector(`input[name="f3_ed_shift"][value="${f1Shift}"]`);
            if (shiftRad) shiftRad.checked = true;
        }

        calcTide();
        calcRain();
        scheduleAutoSave();
    }

    // --- FORM 4 CALCULATIONS ---
    function calcKrabiVitals() {
        const sbp = parseFloat(document.getElementById('f4_sbp')?.value);
        const dbp = parseFloat(document.getElementById('f4_dbp')?.value);
        const hr = parseFloat(document.getElementById('f4_hr')?.value);

        let map = null;
        if (!isNaN(sbp) && !isNaN(dbp)) {
            map = Math.round(((sbp + 2 * dbp) / 3) * 10) / 10;
            document.getElementById('f4_map').value = map;
        } else {
            document.getElementById('f4_map').value = '';
        }

        if (map && !isNaN(hr)) {
            const msi = Math.round((hr / map) * 100) / 100;
            document.getElementById('f4_msi').value = msi.toFixed(2);
        } else {
            document.getElementById('f4_msi').value = '';
        }

        calcDeltaVitals();
        scheduleAutoSave();
    }

    function calcDeltaKillip() {
        const lantaKillip = document.querySelector('input[name="f1_killip"]:checked')?.value;
        const krabiKillip = document.querySelector('input[name="f4_killip"]:checked')?.value;

        if (lantaKillip) document.getElementById('f4_delta_killip_from').value = lantaKillip;
        if (krabiKillip) document.getElementById('f4_delta_killip_to').value = krabiKillip;

        if (lantaKillip && krabiKillip) {
            let kVal = 1;
            if (krabiKillip === '1_2') kVal = 1.5;
            else if (krabiKillip === '3') kVal = 3;
            else if (krabiKillip === '4') kVal = 4;

            const lVal = parseFloat(lantaKillip);
            const diff = kVal - lVal;

            if (diff >= 1 || krabiKillip === '4') {
                document.getElementById('f4_killip_deter').checked = true;
            } else {
                document.getElementById('f4_killip_stable').checked = true;
            }
        }
        calcCompositeDeterioration();
        scheduleAutoSave();
    }

    function calcDeltaGCS() {
        const lGCS = parseInt(document.getElementById('f1_gcs_total')?.value, 10);
        const kGCS_mon = parseInt(document.getElementById('f2_mon4_gcs')?.value, 10);
        
        if (!isNaN(lGCS) && !isNaN(kGCS_mon)) {
            const diff = kGCS_mon - lGCS;
            document.getElementById('f4_delta_gcs').value = (diff > 0 ? '+' : '') + diff;
            if (diff <= -2) {
                document.getElementById('f4_gcs_deter').checked = true;
            } else {
                document.getElementById('f4_gcs_stable').checked = true;
            }
        }
        calcCompositeDeterioration();
    }

    function calcDeltaRTS() {
        const lRTS = parseFloat(document.getElementById('f1_rts_total')?.value);
        const kSBP = parseFloat(document.getElementById('f4_sbp')?.value);
        const kRR = parseFloat(document.getElementById('f4_rr')?.value);
        const kGCS = parseInt(document.getElementById('f2_mon4_gcs')?.value || document.getElementById('f1_gcs_total')?.value, 10);

        if (!isNaN(lRTS) && !isNaN(kSBP) && !isNaN(kRR) && !isNaN(kGCS)) {
            let cGCS = (kGCS >= 13) ? 4 : (kGCS >= 9 ? 3 : (kGCS >= 6 ? 2 : (kGCS >= 4 ? 1 : 0)));
            let cSBP = (kSBP > 89) ? 4 : (kSBP >= 76 ? 3 : (kSBP >= 50 ? 2 : (kSBP >= 1 ? 1 : 0)));
            let cRR = (kRR >= 10 && kRR <= 29) ? 4 : (kRR > 29 ? 3 : (kRR >= 6 ? 2 : (kRR >= 1 ? 1 : 0)));
            const kRTS = Math.round((0.9368 * cGCS + 0.7326 * cSBP + 0.2908 * cRR) * 1000) / 1000;

            const diff = Math.round((kRTS - lRTS) * 1000) / 1000;
            document.getElementById('f4_delta_rts').value = (diff > 0 ? '+' : '') + diff.toFixed(3);

            if (diff <= -1.0) {
                document.getElementById('f4_rts_deter').checked = true;
            } else {
                document.getElementById('f4_rts_stable').checked = true;
            }
        }
        calcCompositeDeterioration();
    }

    function calcDeltaVitals() {
        // MAP Delta
        const lMAP = parseFloat(document.getElementById('f1_map')?.value);
        const kMAP = parseFloat(document.getElementById('f4_map')?.value);
        if (!isNaN(lMAP) && !isNaN(kMAP)) {
            const diffMAP = Math.round((kMAP - lMAP) * 10) / 10;
            document.getElementById('f4_delta_map').value = (diffMAP > 0 ? '+' : '') + diffMAP;
            if (diffMAP < 0) {
                document.getElementById('f4_map_deter').checked = true;
            } else {
                document.getElementById('f4_map_stable').checked = true;
            }
        }

        // MSI Delta
        const lMSI = parseFloat(document.getElementById('f1_msi')?.value);
        const kMSI = parseFloat(document.getElementById('f4_msi')?.value);
        if (!isNaN(lMSI) && !isNaN(kMSI)) {
            const diffMSI = Math.round((kMSI - lMSI) * 100) / 100;
            document.getElementById('f4_delta_msi').value = (diffMSI > 0 ? '+' : '') + diffMSI.toFixed(2);
            if (diffMSI >= 0.15) {
                document.getElementById('f4_msi_deter').checked = true;
            } else {
                document.getElementById('f4_msi_stable').checked = true;
            }
        }

        calcCompositeDeterioration();
    }

    function calcDeltaBT() {
        const lBT = parseFloat(document.getElementById('f1_bt')?.value);
        const kBT = parseFloat(document.getElementById('f4_bt')?.value);
        if (!isNaN(lBT) && !isNaN(kBT)) {
            const diffBT = Math.round((kBT - lBT) * 10) / 10;
            document.getElementById('f4_delta_bt').value = (diffBT > 0 ? '+' : '') + diffBT;
            if (kBT < 35.0) {
                document.getElementById('f4_bt_hypo').checked = true;
            } else {
                document.getElementById('f4_bt_normal').checked = true;
            }
        }
        calcCompositeDeterioration();
    }

    function calcCompositeDeterioration() {
        const kDeter = document.getElementById('f4_killip_deter')?.checked;
        const gDeter = document.getElementById('f4_gcs_deter')?.checked;
        const rDeter = document.getElementById('f4_rts_deter')?.checked;
        const mDeter = document.getElementById('f4_msi_deter')?.checked;
        const pDeter = document.getElementById('f4_map_deter')?.checked;
        const bDeter = document.getElementById('f4_bt_hypo')?.checked;
        const aeEvent = document.getElementById('f2_comp_event')?.checked;

        const isDeter = (kDeter || gDeter || rDeter || mDeter || pDeter || bDeter || aeEvent);
        if (isDeter) {
            document.getElementById('f4_deter_event').checked = true;
        } else {
            document.getElementById('f4_deter_stable').checked = true;
        }
        scheduleAutoSave();
    }

    function calcForm4Timelines() {
        const t4Date = document.getElementById('f4_t4_date')?.value;
        const t4Time = document.getElementById('f4_t4_time')?.value;
        const t5Date = document.getElementById('f4_t5_date')?.value;
        const t5Time = document.getElementById('f4_t5_time')?.value;

        if (t4Time && t5Time) {
            const d2i = diffMinutes(t4Date, t4Time, t5Date, t5Time);
            if (d2i !== null) {
                document.getElementById('f4_t4_5_min').value = d2i;
            }
        }
        calcGoldenWindows();
        scheduleAutoSave();
    }

    function calcGoldenWindows() {
        const t0Date = document.getElementById('f1_t0_date')?.value;
        const t0Time = document.getElementById('f1_t0_time')?.value;
        const oDate = document.getElementById('f1_onset_date')?.value;
        const oTime = document.getElementById('f1_onset_time')?.value;

        // 1. STEMI Door-to-Balloon
        const wireTime = document.getElementById('f4_pci_wire_time')?.value;
        const t5Date = document.getElementById('f4_t5_date')?.value || t0Date;
        if (t0Time && wireTime) {
            const d2b = diffMinutes(t0Date, t0Time, t5Date, wireTime);
            if (d2b !== null) {
                document.getElementById('f4_pci_d2b_min').value = d2b;
                if (d2b <= 180) document.getElementById('f4_pci_achieved').checked = true;
                else document.getElementById('f4_pci_missed').checked = true;
            }
        }

        // 2. Stroke Onset to Needle
        const rtpaTime = document.getElementById('f4_rtpa_time')?.value;
        if (oTime && rtpaTime) {
            const o2n = diffMinutes(oDate, oTime, t5Date, rtpaTime);
            if (o2n !== null) {
                document.getElementById('f4_stroke_o2n_min').value = o2n;
                if (o2n <= 270) document.getElementById('f4_stroke_achieved').checked = true;
                else document.getElementById('f4_stroke_missed').checked = true;
            }
        }

        // 3. Trauma Door to OR
        const orTime = document.getElementById('f4_or_time')?.value;
        if (t0Time && orTime) {
            const d2or = diffMinutes(t0Date, t0Time, t5Date, orTime);
            if (d2or !== null) {
                document.getElementById('f4_trauma_d2or_min').value = d2or;
                if (d2or <= 180) document.getElementById('f4_trauma_achieved').checked = true;
                else document.getElementById('f4_trauma_missed').checked = true;
            }
        }
    }

    function calcAll() {
        calcScreening();
        calcCCI();
        calcVitals();
        calcGCS();
        calcRTS();
        calcTimelines();
        calcForm2Timelines();
        calcCompositeAE();
        calcForm3();
        calcKrabiVitals();
        calcDeltaKillip();
        calcDeltaGCS();
        calcDeltaRTS();
        calcDeltaVitals();
        calcDeltaBT();
        calcForm4Timelines();
    }

    // --- CASE MANAGEMENT & LOCAL STORAGE ---
    let autoSaveTimeout = null;

    function scheduleAutoSave() {
        clearTimeout(autoSaveTimeout);
        autoSaveTimeout = setTimeout(() => {
            saveCurrentCase(true);
        }, 800);
    }

    function initAutoSave() {
        document.querySelectorAll('input, select').forEach(el => {
            el.addEventListener('change', scheduleAutoSave);
            el.addEventListener('input', scheduleAutoSave);
        });
    }

    function getFormData() {
        const data = {};
        document.querySelectorAll('input, select').forEach(el => {
            if (el.type === 'radio') {
                if (el.checked) data[el.name] = el.value;
            } else if (el.type === 'checkbox') {
                data[el.id || el.name] = el.checked;
            } else {
                data[el.id || el.name] = el.value;
            }
        });
        return data;
    }

    function setFormData(data) {
        if (!data) return;
        document.querySelectorAll('input, select').forEach(el => {
            const key = el.id || el.name;
            if (el.type === 'radio') {
                if (data[el.name] !== undefined && el.value === data[el.name]) {
                    el.checked = true;
                }
            } else if (el.type === 'checkbox') {
                if (data[key] !== undefined) {
                    el.checked = Boolean(data[key]);
                }
            } else {
                if (data[key] !== undefined) {
                    el.value = data[key];
                }
            }
        });
        calcAll();
    }

    function saveCurrentCase(isAuto = false) {
        const studyId = document.getElementById('f1_study_id')?.value.trim() || 'UNNAMED';
        const key = 'online_crf_case_' + studyId;
        const formData = getFormData();
        formData.lastUpdated = new Date().toISOString();
        formData.studyId = studyId;

        localStorage.setItem(key, JSON.stringify(formData));
        localStorage.setItem('online_crf_last_active_id', studyId);

        // Update Case Index
        let index = JSON.parse(localStorage.getItem('online_crf_case_index') || '[]');
        if (!index.includes(studyId)) {
            index.push(studyId);
            localStorage.setItem('online_crf_case_index', JSON.stringify(index));
            loadCaseIndex();
        }

        const statusEl = document.getElementById('save-status');
        if (statusEl) {
            const timeStr = new Date().toLocaleTimeString();
            statusEl.innerHTML = '✓ ' + (isAuto ? 'บันทึกอัตโนมัติ' : 'บันทึกเรียบร้อย') + ' (' + timeStr + ')';
            statusEl.style.display = 'inline-flex';
        }
    }

    function loadCaseIndex() {
        const select = document.getElementById('case-selector');
        if (!select) return;
        const index = JSON.parse(localStorage.getItem('online_crf_case_index') || '[]');
        select.innerHTML = '<option value="">-- เลือกเคสที่บันทึกไว้ --</option>';
        index.forEach(id => {
            const opt = document.createElement('option');
            opt.value = id;
            opt.textContent = 'LANTA_' + id;
            select.appendChild(opt);
        });
        const curId = document.getElementById('f1_study_id')?.value.trim();
        if (curId && index.includes(curId)) select.value = curId;
    }

    function onCaseSelected(sel) {
        const id = sel.value;
        if (id) loadCase(id);
    }

    function loadCase(studyId) {
        const raw = localStorage.getItem('online_crf_case_' + studyId);
        if (!raw) return;
        const data = JSON.parse(raw);
        setFormData(data);
        localStorage.setItem('online_crf_last_active_id', studyId);
        loadCaseIndex();
    }

    function createNewCase() {
        if (confirm('ต้องการสร้างเคสใหม่ใช่หรือไม่? (ข้อมูลปัจจุบันได้รับการบันทึกแล้ว)')) {
            const index = JSON.parse(localStorage.getItem('online_crf_case_index') || '[]');
            let nextNum = (index.length + 1).toString().padStart(3, '0');
            
            // Clear inputs
            document.querySelectorAll('input:not([type="radio"]):not([type="checkbox"])').forEach(el => el.value = '');
            document.querySelectorAll('input[type="radio"], input[type="checkbox"]').forEach(el => el.checked = false);

            document.getElementById('f1_study_id').value = nextNum;
            syncFields('study-id-sync', nextNum);
            
            calcAll();
            saveCurrentCase(false);
            switchTab(1);
        }
    }

    // --- EXCEL EXPORT (SHEETJS) ---
    function exportToExcel() {
        if (typeof XLSX === 'undefined') {
            alert('ไม่พบไลบรารี SheetJS กรุณาตรวจสอบไฟล์ xlsx.full.min.js ในโฟลเดอร์');
            return;
        }

        saveCurrentCase(false);

        const index = JSON.parse(localStorage.getItem('online_crf_case_index') || '[]');
        if (index.length === 0) {
            alert('ไม่มีข้อมูลเคสสำหรับ Export');
            return;
        }

        const wb = XLSX.utils.book_new();

        const masterRows = [];
        const form1Rows = [];
        const form2Rows = [];
        const form3Rows = [];
        const form4Rows = [];

        index.forEach(id => {
            const raw = localStorage.getItem('online_crf_case_' + id);
            if (!raw) return;
            const c = JSON.parse(raw);

            // Master Flattened Row (Best for Stata/SPSS/R)
            masterRows.push({
                STUDY_ID: 'LANTA_' + (c.f1_study_id || id),
                Refer_ID: c.f1_refer_id || '',
                HN: c.f1_hn || '',
                VN: c.f1_vn || '',
                Abstract_Date: c.f1_abs_date || '',
                Abstractor: c.f1_abstractor || '',
                Eligible_Status: c.f1_eligible || '',
                Age: c.f1_age || '',
                Sex: c.f1_sex || '',
                Residency: c.f1_residency || '',
                Nationality: c.f1_nationality || '',
                Premorbid_mRS: c.f1_premrs || '',
                CCI_Total: c.f1_cci_total || '',
                Onset_Date: c.f1_onset_date || '',
                Onset_Time: c.f1_onset_time || '',
                Onset_to_ER_min: c.f1_onset_to_er || '',
                T0_Date: c.f1_t0_date || '',
                T0_Time: c.f1_t0_time || '',
                Arrival_Mode: c.f1_arrival_mode || '',
                Triage_ESI: c.f1_esi || '',
                ED_Shift: c.f1_shift || '',
                Disease_STEMI: c.f1_inc4_stemi ? 1 : 0,
                Disease_AIS: c.f1_inc4_ais ? 1 : 0,
                Disease_Trauma: c.f1_inc4_trauma ? 1 : 0,
                Lanta_Killip: c.f1_killip || '',
                Lanta_Stroke_GCS: c.f1_stroke_gcs || '',
                Lanta_Trauma_Acuity: c.f1_trauma_acuity || '',
                Lanta_SBP: c.f1_sbp || '',
                Lanta_DBP: c.f1_dbp || '',
                Lanta_MAP: c.f1_map || '',
                Lanta_HR: c.f1_hr || '',
                Lanta_RR: c.f1_rr || '',
                Lanta_SpO2: c.f1_spo2 || '',
                Lanta_BT: c.f1_bt || '',
                Lanta_MSI: c.f1_msi || '',
                Lanta_Total_GCS: c.f1_gcs_total || '',
                Lanta_Total_RTS: c.f1_rts_total || '',
                PreIntubation: c.f1_intubation || '',
                PreInotropes: c.f1_inotropes || '',
                T1_Date: c.f1_t1_date || '',
                T1_Time: c.f1_t1_time || '',
                T0_1_DIDO_min: c.f1_dido_min || '',
                DIDO_Eval: c.f1_dido_eval || '',
                // Form 2
                Ambulance_Plate: c.f2_amb_plate || '',
                Escort_RN: c.f2_escort_rn || '',
                Driver: c.f2_driver || '',
                T2_Port_Date: c.f2_t2_date || '',
                T2_Port_Time: c.f2_t2_time || '',
                T3_Embark_Date: c.f2_t3_embark_date || '',
                T3_Embark_Time: c.f2_t3_embark_time || '',
                T3_Disembark_Date: c.f2_t3_disembark_date || '',
                T3_Disembark_Time: c.f2_t3_disembark_time || '',
                T4_Krabi_Date: c.f2_t4_date || '',
                T4_Krabi_Time: c.f2_t4_time || '',
                T5_Definitive_Date: c.f2_t5_date || '',
                T5_Definitive_Time: c.f2_t5_time || '',
                T2_IslandRoad_min: c.f2_t2_min || '',
                T3_WaterCrossing_min: c.f2_t3_min || '',
                T_WaitPier_min: c.f2_t_wait_min || '',
                T4_MainlandHwy_min: c.f2_t4_min || '',
                T_Total_min: c.f2_t_total_min || '',
                T5_Definitive_min: c.f2_t5_min || '',
                Ferry_Operate: c.f2_ferry_operate || '',
                Pier_Congestion: c.f2_pier_congestion || '',
                Ferry_Count: c.f2_ferry_count || '',
                Composite_InTransit_AE: c.f2_composite_ae || '',
                // Form 3
                T3_Marine_Date: c.f3_t3_date || '',
                T3_Marine_Time: c.f3_t3_time || '',
                Tide_Height_m: c.f3_tide_height || '',
                Tide_Extreme_Low: c.f3_tide_extreme || '',
                Tide_Phase: c.f3_tide_phase || '',
                Sandbar_Grounding_Risk: c.f3_sandbar_risk || '',
                Season_Monsoon: c.f3_season || '',
                Sea_State: c.f3_sea_state || '',
                Wind_Speed_Knots: c.f3_wind_speed || '',
                Wind_Direction: c.f3_wind_direction || '',
                Precipitation: c.f3_precipitation || '',
                Torrential_Rain_Rate: c.f3_torrential_rain || '',
                Rainfall_Hourly_mm: c.f3_rainfall_mm || '',
                Holiday_Status: c.f3_holiday || '',
                Ferry_Shift_Hours: c.f3_ferry_shift || '',
                // Form 4
                Krabi_HN: c.f4_krabi_hn || '',
                Krabi_Ward: c.f4_ward || '',
                Krabi_SBP: c.f4_sbp || '',
                Krabi_DBP: c.f4_dbp || '',
                Krabi_MAP: c.f4_map || '',
                Krabi_HR: c.f4_hr || '',
                Krabi_RR: c.f4_rr || '',
                Krabi_SpO2: c.f4_spo2 || '',
                Krabi_BT: c.f4_bt || '',
                Krabi_MSI: c.f4_msi || '',
                Krabi_Killip: c.f4_killip || '',
                Delta_Killip_Eval: c.f4_eval_killip || '',
                Delta_GCS_Score: c.f4_delta_gcs || '',
                Delta_GCS_Eval: c.f4_eval_gcs || '',
                Delta_RTS_Score: c.f4_delta_rts || '',
                Delta_RTS_Eval: c.f4_eval_rts || '',
                Delta_MSI_Score: c.f4_delta_msi || '',
                Delta_MSI_Eval: c.f4_eval_msi || '',
                Delta_MAP_mmHg: c.f4_delta_map || '',
                Delta_MAP_Eval: c.f4_eval_map || '',
                Delta_BT_C: c.f4_delta_bt || '',
                Delta_BT_Eval: c.f4_eval_bt || '',
                Composite_Deterioration: c.f4_composite_deter || '',
                Door_to_Intervention_min: c.f4_t4_5_min || '',
                STEMI_D2B_min: c.f4_pci_d2b_min || '',
                STEMI_GoldenWindow: c.f4_eval_pci || '',
                Stroke_O2N_min: c.f4_stroke_o2n_min || '',
                Stroke_GoldenWindow: c.f4_eval_stroke || '',
                Trauma_D2OR_min: c.f4_trauma_d2or_min || '',
                Trauma_GoldenWindow: c.f4_eval_trauma || '',
                Mortality_ER: c.f4_mort_er || '',
                Mortality_24h: c.f4_mort_24h || '',
                Primary_Death_Cause: c.f4_mort_cause || ''
            });

            // Form 1 specific
            form1Rows.push({
                STUDY_ID: 'LANTA_' + (c.f1_study_id || id),
                Refer_ID: c.f1_refer_id || '',
                HN_Lanta: c.f1_hn || '',
                VN_Lanta: c.f1_vn || '',
                Abstract_Date: c.f1_abs_date || '',
                Abstractor: c.f1_abstractor || '',
                Inclusion_All: c.f1_eligible || '',
                Age: c.f1_age || '',
                Sex: c.f1_sex || '',
                Residency: c.f1_residency || '',
                Nationality: c.f1_nationality || '',
                mRS_Premorbid: c.f1_premrs || '',
                CCI_Total: c.f1_cci_total || '',
                T0_Date: c.f1_t0_date || '',
                T0_Time: c.f1_t0_time || '',
                Onset_Date: c.f1_onset_date || '',
                Onset_Time: c.f1_onset_time || '',
                Onset_to_ER_min: c.f1_onset_to_er || '',
                Arrival_Mode: c.f1_arrival_mode || '',
                Triage_ESI: c.f1_esi || '',
                Island_ED_Shift: c.f1_shift || '',
                Killip_Initial: c.f1_killip || '',
                Stroke_GCS_Conscious: c.f1_stroke_gcs || '',
                Trauma_Mechanism: (c.f1_trauma_mech1 ? 'HighVelocity;' : '') + (c.f1_trauma_mech2 ? 'FallHeight;' : '') + (c.f1_trauma_mech3 ? 'Penetrating;' : ''),
                Trauma_Physiological_Acuity: c.f1_trauma_acuity || '',
                SBP_Lanta: c.f1_sbp || '',
                DBP_Lanta: c.f1_dbp || '',
                MAP_Lanta: c.f1_map || '',
                HR_Lanta: c.f1_hr || '',
                RR_Lanta: c.f1_rr || '',
                SpO2_Lanta: c.f1_spo2 || '',
                BT_Lanta: c.f1_bt || '',
                Hct_Lanta: c.f1_hct || '',
                MSI_Lanta: c.f1_msi || '',
                GCS_Total_Lanta: c.f1_gcs_total || '',
                RTS_Total_Lanta: c.f1_rts_total || '',
                Pre_Intubation: c.f1_intubation || '',
                Pre_Inotropes: c.f1_inotropes || '',
                T1_DoorOut_Date: c.f1_t1_date || '',
                T1_DoorOut_Time: c.f1_t1_time || '',
                T0_1_DIDO_min: c.f1_dido_min || '',
                DIDO_Evaluation: c.f1_dido_eval || ''
            });

            // Form 2 specific
            form2Rows.push({
                STUDY_ID: 'LANTA_' + (c.f2_study_id || id),
                Ambulance_Plate: c.f2_amb_plate || '',
                Escort_RN: c.f2_escort_rn || '',
                Driver: c.f2_driver || '',
                T0_Island_ED_Arrival: (c.f2_t0_date || '') + ' ' + (c.f2_t0_time || ''),
                T1_Island_ED_DoorOut: (c.f2_t1_date || '') + ' ' + (c.f2_t1_time || ''),
                T2_Port_Arrival: (c.f2_t2_date || '') + ' ' + (c.f2_t2_time || ''),
                T3_Embark_Ferry: (c.f2_t3_embark_date || '') + ' ' + (c.f2_t3_embark_time || ''),
                T3_Disembark_Port: (c.f2_t3_disembark_date || '') + ' ' + (c.f2_t3_disembark_time || ''),
                T4_Krabi_ED_Door: (c.f2_t4_date || '') + ' ' + (c.f2_t4_time || ''),
                T5_Definitive_Care: (c.f2_t5_date || '') + ' ' + (c.f2_t5_time || ''),
                Interval_T0_1_DIDO_min: c.f2_t0_1_min || '',
                Interval_T2_Road_min: c.f2_t2_min || '',
                Interval_T3_Water_min: c.f2_t3_min || '',
                Interval_WaitPier_min: c.f2_t_wait_min || '',
                Interval_T4_Highway_min: c.f2_t4_min || '',
                Interval_Total_Transit_min: c.f2_t_total_min || '',
                Interval_T5_Definitive_min: c.f2_t5_min || '',
                Ferry_Operation_Shift: c.f2_ferry_operate || '',
                Pier_Congestion_Status: c.f2_pier_congestion || '',
                Active_Ferries_Count: c.f2_ferry_count || '',
                Enroute_Cardiac_Arrest: c.f2_ae_cpr || '',
                Enroute_CPR_Duration_min: c.f2_cpr_duration || '',
                Enroute_Intubation: c.f2_ae_intub || '',
                Enroute_Inotropes_Escalation: c.f2_ae_inotropes || '',
                Enroute_ETT_Dislodgement: c.f2_ae_dislodge || '',
                Enroute_InTransit_Death: c.f2_ae_death || '',
                Composite_InTransit_Deterioration: c.f2_composite_ae || ''
            });

            // Form 3 specific
            form3Rows.push({
                STUDY_ID: 'LANTA_' + (c.f3_study_id || id),
                T3_Date: c.f3_t3_date || '',
                T3_Time: c.f3_t3_time || '',
                Hydro_Station: 'สถานีเกาะลันตาใหญ่ (RTN)',
                Weather_Station: 'สถานีอุตุนิยมวิทยาเกาะลันตา / กระบี่ (TMD)',
                Passage_Coordinates: 'Lat: 7.736 N, Long: 99.062 E',
                Tide_Height_m_LAT: c.f3_tide_height || '',
                Tide_Extreme_Low_Status: c.f3_tide_extreme || '',
                Tide_Phase: c.f3_tide_phase || '',
                Sandbar_Grounding_Risk: c.f3_sandbar_risk || '',
                Season_Monsoon: c.f3_season || '',
                Sea_State: c.f3_sea_state || '',
                Wind_Speed_Knots: c.f3_wind_speed || '',
                Wind_Direction: c.f3_wind_direction || '',
                Precipitation: c.f3_precipitation || '',
                Torrential_Rain_Rate: c.f3_torrential_rain || '',
                Rainfall_Hourly_mm: c.f3_rainfall_mm || '',
                Holiday_Status: c.f3_holiday || '',
                Ferry_Shift: c.f3_ferry_shift || '',
                ED_Shift: c.f3_ed_shift || '',
                RTN_Book_Ref: c.f3_ref_rtn_book ? 1 : 0,
                RTN_Portal_Ref: c.f3_ref_rtn_portal ? 1 : 0,
                RTN_Search_Date: c.f3_ref_rtn_date || '',
                TMD_Hourly_Ref: c.f3_ref_tmd_hourly ? 1 : 0,
                TMD_Portal_Ref: c.f3_ref_tmd_portal ? 1 : 0,
                TMD_Search_Date: c.f3_ref_tmd_date || ''
            });

            // Form 4 specific
            form4Rows.push({
                STUDY_ID: 'LANTA_' + (c.f4_study_id || id),
                HN_Krabi: c.f4_krabi_hn || '',
                T4_Arrival: (c.f4_t4_date || '') + ' ' + (c.f4_t4_time || ''),
                Admitting_Ward: c.f4_ward || '',
                Attending_Physician: c.f4_physician || '',
                SBP_Krabi: c.f4_sbp || '',
                DBP_Krabi: c.f4_dbp || '',
                MAP_Krabi: c.f4_map || '',
                HR_Krabi: c.f4_hr || '',
                RR_Krabi: c.f4_rr || '',
                SpO2_Krabi: c.f4_spo2 || '',
                BT_Krabi: c.f4_bt || '',
                Hct_Krabi: c.f4_hct || '',
                Killip_Krabi: c.f4_killip || '',
                Stroke_GCS_Krabi: c.f4_stroke_gcs || '',
                Trauma_Acuity_Krabi: c.f4_trauma_acuity || '',
                MSI_Krabi: c.f4_msi || '',
                Delta_Killip: c.f4_eval_killip || '',
                Delta_GCS: c.f4_delta_gcs || '',
                Delta_GCS_Eval: c.f4_eval_gcs || '',
                Delta_RTS: c.f4_delta_rts || '',
                Delta_RTS_Eval: c.f4_eval_rts || '',
                Delta_MSI: c.f4_delta_msi || '',
                Delta_MSI_Eval: c.f4_eval_msi || '',
                Delta_MAP: c.f4_delta_map || '',
                Delta_MAP_Eval: c.f4_eval_map || '',
                Delta_BT: c.f4_delta_bt || '',
                Delta_BT_Eval: c.f4_eval_bt || '',
                Composite_Physiological_Deterioration: c.f4_composite_deter || '',
                T5_Definitive_Care: (c.f4_t5_date || '') + ' ' + (c.f4_t5_time || ''),
                Door_to_Intervention_Krabi_min: c.f4_t4_5_min || '',
                STEMI_Wire_Time: c.f4_pci_wire_time || '',
                STEMI_D2B_min: c.f4_pci_d2b_min || '',
                STEMI_Golden_Window: c.f4_eval_pci || '',
                Stroke_rtPA_Time: c.f4_rtpa_time || '',
                Stroke_O2N_min: c.f4_stroke_o2n_min || '',
                Stroke_Golden_Window: c.f4_eval_stroke || '',
                Trauma_OR_Time: c.f4_or_time || '',
                Trauma_D2OR_min: c.f4_trauma_d2or_min || '',
                Trauma_Golden_Window: c.f4_eval_trauma || '',
                Mortality_ER_Immediate: c.f4_mort_er || '',
                Mortality_24h_Post: c.f4_mort_24h || '',
                Primary_Cause_of_Death: c.f4_mort_cause || '',
                ICD10_Cause: c.f4_mort_cause_icd || ''
            });
        });

        // Add Worksheets
        const wsMaster = XLSX.utils.json_to_sheet(masterRows);
        const wsForm1 = XLSX.utils.json_to_sheet(form1Rows);
        const wsForm2 = XLSX.utils.json_to_sheet(form2Rows);
        const wsForm3 = XLSX.utils.json_to_sheet(form3Rows);
        const wsForm4 = XLSX.utils.json_to_sheet(form4Rows);

        XLSX.utils.book_append_sheet(wb, wsMaster, 'Master_Cohort_Dataset');
        XLSX.utils.book_append_sheet(wb, wsForm1, 'Form_1_Island_ED');
        XLSX.utils.book_append_sheet(wb, wsForm2, 'Form_2_MicroTimeline');
        XLSX.utils.book_append_sheet(wb, wsForm3, 'Form_3_Marine_Weather');
        XLSX.utils.book_append_sheet(wb, wsForm4, 'Form_4_Mainland_Care');

        const nowStr = new Date().toISOString().slice(0, 10);
        XLSX.writeFile(wb, 'Emergency_Transfer_CRF_Master_Database_' + nowStr + '.xlsx');
    }
    """
'''

with open('/Users/nuttp./Desktop/MSc CU/Thesis/CRF/Online_CRF/build_js.py', 'w', encoding='utf-8') as f:
    f.write(js_code)
print("Successfully updated build_js.py with Form 3 integration")
