"""
Marketing & Commercialization Page for CropSense (fixed)
Fixes:
 - Use a single embedded HTML component for Business Model + Pricing Plans
   to isolate CSS from Streamlit theme and avoid Markdown code-block issues.
 - Keep Streamlit interactive buttons under pricing cards so they remain functional.
 - Dedent other HTML sections so Streamlit doesn't render them as code blocks.
"""
import streamlit as st
import os
import sys
import textwrap
from datetime import datetime

# If you have a modern_footer module in parent dir (optional)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from modern_footer import render_modern_footer
except Exception:
    # If modern_footer not available, define a no-op to avoid breaking the app
    def render_modern_footer():
        pass

# Page configuration
st.set_page_config(
    page_title="CropSense - Commercialization",
    page_icon="💰",
    layout="wide"
)

# Helper to dedent and render HTML via st.markdown where appropriate
def render_html(md: str):
    st.markdown(textwrap.dedent(md), unsafe_allow_html=True)


# HERO SECTION (dedented)
render_html("""
<div class="hero-modern" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 3.2rem 1.5rem; border-radius: 18px; margin-bottom: 2rem; text-align:center;">
    <div style="font-size: 3.8rem; margin-bottom: 1rem;">💰</div>
    <div style="font-size:2.8rem; font-weight:800; margin-bottom:0.6rem;">Commercialization</div>
    <div style="font-size:1.05rem; opacity:0.95; line-height:1.5; max-width:1100px; margin:0 auto;">
        Transform Your Agricultural Business with CropSense AI Solutions — Scalable Pricing Plans for Farms of All Sizes
    </div>
</div>
""")

# Combined isolated HTML for Business Model + Pricing Plans (use an iframe via components.html)
business_pricing_html = textwrap.dedent("""
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<style>
/* Reset minor defaults inside iframe */
* { box-sizing: border-box; font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; }

/* Section titles */
.section-title { text-align:center; margin: 30px 0 10px; font-size: 2.2rem; font-weight: 800; background: linear-gradient(45deg,#2E8B57,#4ECDC4); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.section-subtitle { text-align:center; color:#666; margin-bottom:24px; font-size:1rem; max-width:1000px; margin-left:auto; margin-right:auto; }

/* Grid wrappers */
.business-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px; margin: 28px 0 48px; max-width: 1300px; margin-left:auto; margin-right:auto; padding: 0 12px; }
.pricing-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 18px 0 40px; max-width: 1400px; margin-left:auto; margin-right:auto; padding: 0 12px; }

/* Business-model card */
.business-card {
    background: linear-gradient(135deg, #f5f7fa 0%, #cfe3f0 100%);
    border-radius: 14px;
    padding: 20px;
    border-left: 6px solid #667eea;
    min-height: 220px;
    box-shadow: 0 14px 30px rgba(14,20,30,0.06);
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.revenue-badge { color:#667eea; font-weight:700; font-size:0.85rem; text-transform:uppercase; letter-spacing:0.6px; margin-bottom:4px; }
.business-title { color:#2c3e50; font-size:1.25rem; font-weight:800; margin-bottom:6px; }
.business-desc { color:#444; font-size:0.95rem; line-height:1.5; margin-bottom:8px; }

/* custom list */
.custom-list { padding-left: 14px; margin-top:8px; }
.custom-list-item { position: relative; padding-left: 18px; margin: 8px 0; color:#444; }
.custom-list-item:before { content: "•"; position:absolute; left:0; color:#667eea; font-weight:800; }

/* Pricing card (white) */
.pricing-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 18px;
    box-shadow: 0 10px 24px rgba(6,10,20,0.06);
    border: 1px solid rgba(102,126,234,0.06);
    display: flex;
    flex-direction: column;
    min-height: 260px;
    justify-content: space-between;
}
.pricing-card.popular { border: 2px solid #667eea; }
.popular-badge {
    display:inline-block;
    background: linear-gradient(135deg,#667eea,#764ba2);
    color:white;
    padding:6px 12px;
    border-radius:18px;
    font-size:0.78rem;
    font-weight:700;
    margin-bottom:8px;
}
.price { font-size:2.4rem; font-weight:800; background: linear-gradient(45deg,#667eea,#764ba2); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin: 6px 0; }
.price-sub { color:#666; font-size:0.95rem; margin-bottom:10px; }
.feature-list { text-align:left; margin-top:8px; padding-left:14px; }
.feature-list li { margin:6px 0; color:#444; }

/* small responsive */
@media (max-width: 1100px) {
    .business-grid { grid-template-columns: 1fr; }
    .pricing-grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 640px) {
    .pricing-grid { grid-template-columns: 1fr; }
}

/* quick helpers */
.container { padding: 12px 8px; }
.card-cta { text-align: center; margin-top: 12px; font-size:0.95rem; color:#333; }
</style>
</head>
<body>
<div class="container">

  <!-- Business Model Section -->
  <div style="margin-top:6px;">
    <div class="section-title">Business Model</div>
    <div class="section-subtitle">Sustainable revenue streams driving agricultural innovation forward</div>
  </div>

  <div class="business-grid">
    <div class="business-card">
      <div class="business-title">🚜 SaaS Subscriptions</div>
      <div class="revenue-badge">Primary Revenue Stream</div>
      <div class="business-desc">Monthly/annual subscriptions for individual farmers and agricultural enterprises.</div>
      <div>
        <div style="font-weight:700; color:#2c3e50; margin-bottom:6px;">Key Features:</div>
        <div class="custom-list">
          <div class="custom-list-item">Tiered pricing based on farm size</div>
          <div class="custom-list-item">Feature-based packages</div>
          <div class="custom-list-item">Volume discounts for cooperatives</div>
        </div>
      </div>
    </div>

    <div class="business-card">
      <div class="business-title">🏢 Enterprise Solutions</div>
      <div class="revenue-badge">B2B Revenue</div>
      <div class="business-desc">Custom AI solutions for large agricultural corporations and government agencies.</div>
      <div>
        <div style="font-weight:700; color:#2c3e50; margin-bottom:6px;">Services Include:</div>
        <div class="custom-list">
          <div class="custom-list-item">Custom model development</div>
          <div class="custom-list-item">API access for integration</div>
          <div class="custom-list-item">White-label solutions</div>
        </div>
      </div>
    </div>

    <div class="business-card">
      <div class="business-title">📊 Data Analytics</div>
      <div class="revenue-badge">Ancillary Revenue</div>
      <div class="business-desc">Aggregated, anonymized data insights for research and market analysis.</div>
      <div>
        <div style="font-weight:700; color:#2c3e50; margin-bottom:6px;">Data Products:</div>
        <div class="custom-list">
          <div class="custom-list-item">Market trend reports</div>
          <div class="custom-list-item">Research partnerships</div>
          <div class="custom-list-item">Insurance industry data</div>
        </div>
      </div>
    </div>
  </div>

  <!-- Pricing Plans Section -->
  <div style="margin-top:36px;">
    <div class="section-title">Pricing Plans</div>
    <div class="section-subtitle">Choose the perfect plan for your farming operation</div>
  </div>

  <div class="pricing-grid">
    <div class="pricing-card">
      <div>
        <div style="font-size:1.05rem; color:#2c3e50; font-weight:700;">🌱 Starter</div>
        <div style="color:#666; margin-bottom:6px;">For Small Farms</div>
        <div class="price">$19</div>
        <div class="price-sub">per month</div>
        <ul class="feature-list">
          <li>Up to 50 acres</li>
          <li>Basic yield predictions</li>
          <li>Weather integration</li>
          <li>Mobile app access</li>
        </ul>
      </div>
      <div class="card-cta">Best for hobby farms & early adopters</div>
    </div>

    <div class="pricing-card popular">
      <div>
        <div class="popular-badge">Most Popular</div>
        <div style="font-size:1.05rem; color:#2c3e50; font-weight:700;">🚜 Professional</div>
        <div style="color:#666; margin-bottom:6px;">For Growing Farms</div>
        <div class="price">$49</div>
        <div class="price-sub">per month</div>
        <ul class="feature-list">
          <li>Up to 500 acres</li>
          <li>Advanced predictions</li>
          <li>Satellite monitoring</li>
          <li>Soil analysis</li>
        </ul>
      </div>
      <div class="card-cta">Popular among small commercial farms</div>
    </div>

    <div class="pricing-card">
      <div>
        <div style="font-size:1.05rem; color:#2c3e50; font-weight:700;">🏢 Enterprise</div>
        <div style="color:#666; margin-bottom:6px;">For Large Operations</div>
        <div class="price">$99</div>
        <div class="price-sub">per month</div>
        <ul class="feature-list">
          <li>Unlimited acres</li>
          <li>Custom AI models</li>
          <li>Real-time satellite feeds</li>
          <li>Dedicated support</li>
        </ul>
      </div>
      <div class="card-cta">Custom contracts & SLAs available</div>
    </div>

    <div class="pricing-card">
      <div>
        <div style="font-size:1.05rem; color:#2c3e50; font-weight:700;">🤝 Government</div>
        <div style="color:#666; margin-bottom:6px;">Public Sector</div>
        <div class="price">Custom</div>
        <div class="price-sub">contact us</div>
        <ul class="feature-list">
          <li>Regional monitoring</li>
          <li>Policy planning tools</li>
          <li>Disaster prediction</li>
          <li>Multi-farm management</li>
        </ul>
      </div>
      <div class="card-cta">Co-designed programs for agencies</div>
    </div>

  </div>

</div>
</body>
</html>
""")

# Render the combined HTML as an isolated iframe so theme/CSS won't override it
# Height tuned to accommodate both sections; adjust if needed.
st.components.v1.html(business_pricing_html, height=760, scrolling=True)


# Add interactive Streamlit buttons below the pricing cards (so they stay functional)
st.markdown("")  # small spacer
btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
with btn_col1:
    if st.button("Start Free Trial — Starter", key="starter_trial"):
        st.success("🎉 Starter free trial activated! 14 days of access.")
with btn_col2:
    if st.button("Start Free Trial — Professional", key="pro_trial"):
        st.success("🎉 Professional free trial activated! 14 days of access.")
with btn_col3:
    if st.button("Contact Sales — Enterprise", key="enterprise_contact"):
        st.info("📧 Our sales team will contact you within 24 hours.")
with btn_col4:
    if st.button("Request Demo — Government", key="gov_demo"):
        st.info("📅 We'll schedule a customized demo for your agency.")


# REVENUE PROJECTIONS (use normal Streamlit cards for these)
render_html("""
<div style="margin-top:28px;">
  <div style="text-align:center; font-size:1.9rem; font-weight:800; margin-bottom:6px; background: linear-gradient(45deg,#2E8B57,#4ECDC4); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">Market Opportunity</div>
  <div style="text-align:center; color:#666; margin-bottom:18px;">Projected growth and revenue potential in the precision agriculture market</div>
</div>
""")

rev_col1, rev_col2, rev_col3, rev_col4 = st.columns(4, gap="large")
with rev_col1:
    render_html("""
    <div style="background:#fff; padding:18px; border-radius:12px; text-align:center; box-shadow: 0 8px 18px rgba(0,0,0,0.06);">
        <div style="font-size:1.6rem; font-weight:800; background: linear-gradient(45deg,#667eea,#764ba2); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">$12.9B</div>
        <div style="font-size:0.9rem; color:#666; margin-top:6px;">Market Size 2024</div>
    </div>
    """)
with rev_col2:
    render_html("""
    <div style="background:#fff; padding:18px; border-radius:12px; text-align:center; box-shadow: 0 8px 18px rgba(0,0,0,0.06);">
        <div style="font-size:1.6rem; font-weight:800; background: linear-gradient(45deg,#667eea,#764ba2); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">$22.8B</div>
        <div style="font-size:0.9rem; color:#666; margin-top:6px;">Market Size 2028</div>
    </div>
    """)
with rev_col3:
    render_html("""
    <div style="background:#fff; padding:18px; border-radius:12px; text-align:center; box-shadow: 0 8px 18px rgba(0,0,0,0.06);">
        <div style="font-size:1.6rem; font-weight:800; background: linear-gradient(45deg,#667eea,#764ba2); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">45%</div>
        <div style="font-size:0.9rem; color:#666; margin-top:6px;">CAGR Growth</div>
    </div>
    """)
with rev_col4:
    render_html("""
    <div style="background:#fff; padding:18px; border-radius:12px; text-align:center; box-shadow: 0 8px 18px rgba(0,0,0,0.06);">
        <div style="font-size:1.6rem; font-weight:800; background: linear-gradient(45deg,#667eea,#764ba2); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">500K+</div>
        <div style="font-size:0.9rem; color:#666; margin-top:6px;">Target Farms</div>
    </div>
    """)


# Partnerships / contact CTA (kept as before)
render_html("""
<div style="margin-top:28px;">
  <div style="text-align:center; font-size:1.6rem; font-weight:800; margin-bottom:8px; background: linear-gradient(45deg,#2E8B57,#4ECDC4); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">Partnership Opportunities</div>
  <div style="text-align:center; color:#666; margin-bottom:14px;">Strategic alliances driving market penetration and innovation</div>
</div>
""")

partner_col1, partner_col2 = st.columns(2, gap="large")
with partner_col1:
    render_html("""
    <div style="background:#fff; padding:18px; border-radius:12px; box-shadow: 0 10px 24px rgba(0,0,0,0.06); margin-bottom:12px;">
      <div style="font-size:2rem; margin-bottom:8px;">🤝</div>
      <div style="font-weight:700; color:#2c3e50; margin-bottom:6px;">Technology Partners</div>
      <div style="color:#444;">Integration Opportunities: Farm equipment manufacturers, weather providers, satellite imagery, IoT sensors.</div>
    </div>
    """)
    render_html("""
    <div style="background:#fff; padding:18px; border-radius:12px; box-shadow: 0 10px 24px rgba(0,0,0,0.06);">
      <div style="font-size:2rem; margin-bottom:8px;">🏛️</div>
      <div style="font-weight:700; color:#2c3e50; margin-bottom:6px;">Government & Research</div>
      <div style="color:#444;">USDA partnerships, agricultural extension programs, climate-change mitigation, food security initiatives.</div>
    </div>
    """)
with partner_col2:
    render_html("""
    <div style="background:#fff; padding:18px; border-radius:12px; box-shadow: 0 10px 24px rgba(0,0,0,0.06); margin-bottom:12px;">
      <div style="font-size:2rem; margin-bottom:8px;">📈</div>
      <div style="font-weight:700; color:#2c3e50; margin-bottom:6px;">Distribution Partners</div>
      <div style="color:#444;">Agricultural cooperatives, farm supply retailers, consultants, insurance companies.</div>
    </div>
    """)
    render_html("""
    <div style="background:#fff; padding:18px; border-radius:12px; box-shadow: 0 10px 24px rgba(0,0,0,0.06);">
      <div style="font-size:2rem; margin-bottom:8px;">🌍</div>
      <div style="font-weight:700; color:#2c3e50; margin-bottom:6px;">International Expansion</div>
      <div style="color:#444;">Target Markets: North America, EU, Asia-Pacific, Latin America.</div>
    </div>
    """)

# Contact CTA and quick action buttons
render_html("""
<div style="background: linear-gradient(135deg,#667eea 0%, #764ba2 100%); color:white; padding:24px; border-radius:12px; margin-top:24px; text-align:center;">
  <div style="font-size:1.4rem; font-weight:800; margin-bottom:6px;">Ready to Invest in Agricultural Innovation?</div>
  <div style="opacity:0.95; margin-bottom:14px;">Contact our commercialization team to discuss partnership opportunities</div>
</div>
""")

ct_col1, ct_col2, ct_col3 = st.columns(3, gap="large")
with ct_col1:
    if st.button("📧 Email Our Team (contact@cropsense.ai)", key="email_team2", use_container_width=True):
        st.info("📧 Contact: commercial@cropsense.ai")
with ct_col2:
    if st.button("📞 Schedule Call", key="schedule_call2", use_container_width=True):
        st.info("📅 Our team will contact you within 24 hours")
with ct_col3:
    if st.button("📊 Investor Deck", key="investor_deck2", use_container_width=True):
        st.info("📚 Download our investor presentation")


# Render modern footer if available
render_modern_footer()
