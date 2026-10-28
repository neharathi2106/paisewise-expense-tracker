"""Paisewise — a polished Streamlit expense tracker UI."""
from datetime import date, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from database import (CATEGORIES, initialize_database, get_expenses, add_expense, update_expense,
                      delete_expense, get_monthly_budget, set_monthly_budget)
from analytics import expense_frame, monthly_totals
from algorithms import merge_sort, bubble_sort, binary_search_amount, benchmark_sorts, synthetic_amounts
from ml_prediction import predict_next_month

st.set_page_config(page_title="Paisewise | Your money, understood", page_icon="₹", layout="wide", initial_sidebar_state="expanded")
initialize_database()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
:root{color-scheme:dark;--bg:#0b1020;--panel:#111a2e;--panel2:#151f36;--line:#26334c;--text:#eef3ff;--muted:#96a4bd;--accent:#818cf8;--accent2:#6366f1;--green:#34d399;--amber:#fbbf24;--red:#fb7185}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
.stApp{background:radial-gradient(ellipse at 78% -18%,#293367 0%,transparent 40%),var(--bg);color:var(--text)}
.block-container{max-width:1440px;padding:2.2rem 3rem 4rem}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#10182b,#0d1425);border-right:1px solid #202b41}
[data-testid="stSidebar"]>div{padding-top:1.5rem}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p{color:#9eabc1}
[data-testid="stRadio"] label{border-radius:10px;padding:5px 8px}
[data-testid="stRadio"] label:hover{background:#1a2540}
[data-testid="stMetric"]{background:linear-gradient(145deg,#151f35,#111a2b);padding:19px 21px;border:1px solid #26334c;border-radius:17px;box-shadow:0 10px 30px #03081750;transition:transform .18s,border-color .18s}
[data-testid="stMetric"]:hover{transform:translateY(-2px);border-color:#5764a0}
[data-testid="stMetricLabel"]{color:#9eabc1!important;font-size:.86rem}
[data-testid="stMetricValue"]{color:#f5f7ff!important;font-family:'Manrope',sans-serif;font-weight:700}
[data-testid="stMetricDelta"]{font-size:.78rem}
.stButton>button,.stFormSubmitButton>button{border-radius:10px;border:1px solid #3c4c72;background:linear-gradient(120deg,#6366f1,#7c6cf5);color:white;font-weight:700;padding:.58rem 1rem;transition:all .18s;box-shadow:0 5px 18px #6366f130}
.stButton>button:hover,.stFormSubmitButton>button:hover{border-color:#a5b4fc;transform:translateY(-1px);box-shadow:0 8px 22px #6366f145}
[data-testid="stTextInput"] input,[data-testid="stNumberInput"] input,[data-testid="stDateInput"] input,[data-testid="stTextArea"] textarea,[data-testid="stSelectbox"]>div,[data-testid="stMultiSelect"]>div{background:#111a2d!important;border-color:#2a3854!important;border-radius:10px!important;color:#eef3ff!important}
[data-testid="stProgressBar"]>div{background:#202b42;border-radius:99px;height:10px}
[data-testid="stProgressBar"]>div>div{background:linear-gradient(90deg,#6366f1,#a78bfa);border-radius:99px}
[data-testid="stDataFrame"]{border:1px solid #26334c;border-radius:12px;overflow:hidden}
hr{border-color:#26334c!important}
h1,h2,h3{font-family:'Manrope',sans-serif!important;letter-spacing:-.035em;color:#f4f6ff}
h1{font-size:2.05rem!important} h2{font-size:1.42rem!important} h3{font-size:1.1rem!important}
.stCaption,[data-testid="stCaptionContainer"]{color:#99a7bf}
div[data-testid="stAlert"]{border-radius:12px;border:1px solid #32415f}
.ss-kicker{color:#9ca9c0;font-size:.78rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase}
.ss-hero{font-family:'Manrope',sans-serif;font-size:2.15rem;line-height:1.15;font-weight:800;letter-spacing:-.05em;margin:.25rem 0 .4rem;color:#f7f8ff}
.ss-subtitle{color:#9eabc1;font-size:1rem}
.ss-card{background:linear-gradient(145deg,#151f35,#111a2b);border:1px solid #26334c;border-radius:17px;padding:20px 22px;box-shadow:0 10px 30px #03081738;min-height:128px;transition:transform .18s,border-color .18s}
.ss-card:hover{transform:translateY(-2px);border-color:#5965a1}
.ss-card-label{font-size:.84rem;color:#9eabc1;display:flex;align-items:center;gap:8px}
.ss-card-icon{display:inline-grid;place-items:center;width:28px;height:28px;border-radius:9px;background:#262b55;color:#c4c8ff;font-size:1rem}
.ss-card-value{font-family:'Manrope',sans-serif;font-size:1.55rem;font-weight:800;color:#f5f7ff;margin-top:13px}
.ss-card-foot{font-size:.76rem;color:#8797b2;margin-top:4px}
.ss-section{background:#111a2b;border:1px solid #26334c;border-radius:16px;padding:18px 20px;margin:10px 0}
.ss-empty{background:radial-gradient(ellipse at 50% 0%,#252f60,#121b30 65%);border:1px solid #334169;border-radius:20px;padding:38px;text-align:center;margin:20px 0}
.ss-empty-mark{margin:0 auto 16px;width:54px;height:54px;border-radius:17px;background:#31386b;display:grid;place-items:center;color:#c7ceff;font-size:1.55rem}
.ss-empty h3{margin:0 0 8px}.ss-empty p{color:#a8b4ca;margin:0}
.ss-brand{font-family:'Manrope',sans-serif;color:#f2f4ff;font-size:1.24rem;font-weight:800;letter-spacing:-.04em}.ss-brand span{color:#9b9eff}
@media(max-width:900px){.block-container{padding:1.4rem 1rem 3rem}.ss-hero{font-size:1.8rem}}
</style>
""", unsafe_allow_html=True)

PAGES=["Dashboard","Add Expense","Transactions","Analytics","Budget Planner","AI Spending Insights","ML Expense Prediction","DAA Lab","About Project"]
ICONS={"Dashboard":"▦","Add Expense":"＋","Transactions":"↔","Analytics":"◫","Budget Planner":"◷","AI Spending Insights":"✧","ML Expense Prediction":"⌁","DAA Lab":"⌘","About Project":"ⓘ"}
if "page" not in st.session_state: st.session_state.page="Dashboard"
def go(page): st.session_state.page=page
with st.sidebar:
    st.markdown('<div class="ss-brand">Paisewise</div>',unsafe_allow_html=True)
    st.caption("YOUR MONEY, UNDERSTOOD")
    st.markdown("<br>",unsafe_allow_html=True)
    page=st.radio("Workspace",PAGES,format_func=lambda p:f"{ICONS[p]}   {p}",key="page",label_visibility="collapsed")
    st.markdown("<br><br>",unsafe_allow_html=True)
    st.caption("PERSONAL FINANCE · PBL")
    st.caption("DAA · B.Tech Computer Science")

# One fresh read per rerun keeps all screens connected to the persisted database.
expenses=get_expenses(); df=expense_frame(expenses); budget=get_monthly_budget(); today=pd.Timestamp(date.today())
month_df=df[df.expense_date.dt.to_period("M")==today.to_period("M")] if not df.empty else df
month_spend=float(month_df.amount.sum()) if not month_df.empty else 0.0

def money(value): return f"₹{float(value):,.2f}"
def header(title,subtitle,kicker="PAISAWISE"):
    st.markdown(f'<div class="ss-kicker">{kicker}</div><div class="ss-hero">{title}</div><div class="ss-subtitle">{subtitle}</div>',unsafe_allow_html=True)
def card(label,value,icon,foot=""):
    st.markdown(f'<div class="ss-card"><div class="ss-card-label"><span class="ss-card-icon">{icon}</span>{label}</div><div class="ss-card-value">{value}</div><div class="ss-card-foot">{foot}</div></div>',unsafe_allow_html=True)
def show_table(frame):
    if frame.empty: st.info("No transactions match these filters."); return
    view=frame.copy()
    view["expense_date"]=view.expense_date.dt.strftime("%d %b %Y")
    view["amount"]=view.amount.map(money)
    st.dataframe(view.rename(columns={"id":"ID","title":"Transaction","amount":"Amount","category":"Category","expense_date":"Date","notes":"Notes"}),use_container_width=True,hide_index=True)
def budget_status():
    if not budget: return "Set a monthly budget to see your progress here."
    ratio=month_spend/budget
    if ratio>=1: return f"Monthly budget reached. You are {money(month_spend-budget)} over the limit."
    if ratio>=.8: return f"Heads up: you have used {ratio:.0%} of your monthly budget."
    return f"You have used {ratio:.0%} of your monthly budget."
def category_chart(frame):
    if frame.empty: st.caption("Category chart will appear when transactions are available."); return
    totals=frame.groupby("category").amount.sum().sort_values()
    fig,ax=plt.subplots(figsize=(7,3.8)); fig.patch.set_alpha(0); ax.set_facecolor("#111a2b")
    bars=ax.barh(totals.index,totals.values,color=["#5259ba","#6366f1","#818cf8","#a78bfa","#34d399","#38bdf8"]*(len(totals)//6+1),height=.58)
    ax.spines[:].set_visible(False); ax.tick_params(colors="#aab6cb",labelsize=9); ax.xaxis.grid(True,color="#28344b",linewidth=.7); ax.set_axisbelow(True); ax.set_xlabel("Amount (₹)",color="#8998b1",fontsize=9)
    ax.bar_label(bars,labels=[f"₹{v:,.0f}" for v in totals.values],padding=5,color="#dce4f5",fontsize=8); fig.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close(fig)
def trend_chart(series,kind="line"):
    if len(series)==0: st.caption("Monthly trend will appear when transactions are available."); return
    frame=series.rename("Spending (₹)").to_frame()
    st.line_chart(frame,height=300,color="#818cf8")
def range_filter(frame,key):
    earliest=frame.expense_date.min().date(); latest=max(date.today(),frame.expense_date.max().date())
    dates=st.date_input("Date range",value=(earliest,latest),key=key)
    if isinstance(dates,tuple) and len(dates)==2: return dates
    return dates,dates

# DASHBOARD
if page=="Dashboard":
    header("Paisewise",f"Your money, understood. Welcome back — here’s your financial snapshot for {today.strftime('%B %Y')}.","PERSONAL FINANCE")
    cta,_=st.columns([1,5])
    with cta:
        st.button("＋  Add expense",key="dashboard_add",type="primary",use_container_width=True,on_click=go,args=("Add Expense",))
    st.write("")
    total=float(df.amount.sum()) if not df.empty else 0.0; avg=float(df.amount.mean()) if not df.empty else 0.0
    remaining=max(0,budget-month_spend) if budget else None
    cols=st.columns(4,gap="medium")
    for col,(label,value,icon,foot) in zip(cols,[("Total expenses",money(total),"↗","All recorded transactions"),("This month’s spending",money(month_spend),"◷",today.strftime("%B %Y")),("Remaining budget",money(remaining) if remaining is not None else "Not set","◉","Monthly budget balance"),("Average transaction",money(avg),"⌁",f"Across {len(df)} transactions")]):
        with col: card(label,value,icon,foot)
    if df.empty:
        st.markdown('<div class="ss-empty"><div class="ss-empty-mark">＋</div><h3>Your financial picture starts here</h3><p>Add your first transaction to unlock spending trends, category insights and budget tracking.</p></div>',unsafe_allow_html=True)
        st.button("Add your first expense",type="primary",key="empty_add",on_click=go,args=("Add Expense",))
    else:
        st.write(""); left,right=st.columns([1.35,1],gap="large")
        with left:
            st.subheader("Monthly spending trend")
            trend_chart(monthly_totals(expenses))
        with right:
            st.subheader("Category breakdown")
            category_chart(month_df)
        st.write(""); left,right=st.columns([1.2,.8],gap="large")
        with left:
            st.subheader("Recent transactions")
            recent=df.sort_values(["expense_date","id"],ascending=False).head(6)
            show_table(recent)
        with right:
            st.subheader("Budget progress")
            if budget:
                st.metric("Used this month",f"{month_spend/budget:.0%}",help="Current month spending divided by your monthly budget.")
                st.progress(min(month_spend/budget,1.0)); st.caption(f"{money(month_spend)} spent · {money(max(0,budget-month_spend))} remaining")
                if month_spend>=budget: st.error(budget_status())
                elif month_spend>=budget*.8: st.warning(budget_status())
                else: st.success(budget_status())
            else:
                st.info("Set a monthly budget to track your progress.")
                st.button("Plan a budget",key="dash_budget",on_click=go,args=("Budget Planner",))
            st.markdown('<div class="ss-section"><div class="ss-kicker">THIS MONTH</div>',unsafe_allow_html=True)
            st.metric("Transactions",len(month_df)); st.metric("Daily average",money(month_spend/max(today.day,1)))
            st.markdown('</div>',unsafe_allow_html=True)

# ADD EXPENSE
elif page=="Add Expense":
    header("Add a transaction","Log it once. Your dashboard and insights update automatically.","NEW TRANSACTION")
    st.write(""); left,right=st.columns([1.35,.65],gap="large")
    with left:
        st.markdown('<div class="ss-section">',unsafe_allow_html=True)
        with st.form("add_expense_form",clear_on_submit=True):
            title=st.text_input("Transaction title *",placeholder="e.g. Lunch with friends")
            amount=st.number_input("Amount (₹) *",min_value=0.0,step=50.0,format="%.2f",help="Enter an amount greater than zero.")
            c1,c2=st.columns(2); category=c1.selectbox("Category *",CATEGORIES,format_func=lambda x:{"Food":"◉  Food","Travel":"↗  Travel","Shopping":"◇  Shopping","Education":"▤  Education","Bills":"▧  Bills","Healthcare":"＋  Healthcare","Entertainment":"▷  Entertainment","Other":"○  Other"}.get(x,x)); expense_date=c2.date_input("Date *",value=date.today())
            notes=st.text_area("Notes",placeholder="Optional context for this transaction")
            save_col,clear_col=st.columns([1,1]); submitted=save_col.form_submit_button("Save transaction",type="primary",use_container_width=True); clear_col.form_submit_button("Clear fields",use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)
        if submitted:
            try: add_expense(title,amount,category,expense_date.isoformat(),notes); st.success("Transaction saved. Your totals are refreshed."); st.rerun()
            except ValueError as e: st.error(str(e))
    with right:
        st.markdown('<div class="ss-section"><div class="ss-kicker">QUICK NOTE</div><h3>Good records make better insights.</h3><p style="color:#9eabc1">Use the actual transaction date and a consistent category. The monthly trend and forecast use the dates you enter.</p></div>',unsafe_allow_html=True)
        st.metric("Recorded transactions",len(expenses)); st.metric("This month",money(month_spend))

# TRANSACTIONS
elif page=="Transactions":
    header("Transactions","Search, filter, sort and manage your recorded expenses.","LEDGER")
    if df.empty: st.markdown('<div class="ss-empty"><div class="ss-empty-mark">↔</div><h3>No transactions yet</h3><p>Add your first expense to populate your ledger.</p></div>',unsafe_allow_html=True);
    if not df.empty:
        query=st.text_input("Search by title",placeholder="Search transactions…",key="txn_search")
        col1,col2,col3=st.columns([1,1,1]); cats=sorted(df.category.dropna().unique()); chosen=col1.multiselect("Categories",cats,default=cats,key="txn_categories"); start,end=range_filter(df,"txn_dates")
        sort_by=col2.selectbox("Sort by",["Date","Amount","Title"],key="txn_sort"); direction=col3.radio("Order",["Descending","Ascending"],horizontal=True,key="txn_direction")
        filtered=df[df.category.isin(chosen)&(df.expense_date.dt.date>=start)&(df.expense_date.dt.date<=end)].copy()
        if query.strip(): filtered=filtered[filtered.title.str.contains(query.strip(),case=False,na=False)]
        sort_col={"Date":"expense_date","Amount":"amount","Title":"title"}[sort_by]; filtered=filtered.sort_values(sort_col,ascending=direction=="Ascending")
        st.caption(f"{len(filtered)} transaction{'s' if len(filtered)!=1 else ''} found")
        if filtered.empty: st.info("No results found. Try a different search or filter.")
        else: show_table(filtered)
        if not filtered.empty:
            st.divider(); st.subheader("Edit or delete")
            ids=filtered.id.astype(int).tolist(); selected=st.selectbox("Choose transaction",ids,format_func=lambda i:f"#{i} · {filtered.loc[filtered.id==i,'title'].iloc[0]}",key="txn_selected"); row=next(e for e in expenses if e["id"]==selected)
            with st.expander("Edit transaction",expanded=False):
                with st.form("edit_expense_form"):
                    title=st.text_input("Title",row["title"]); amount=st.number_input("Amount (₹)",min_value=0.0,value=float(row["amount"]),step=50.0); cat=st.selectbox("Category",CATEGORIES,index=CATEGORIES.index(row["category"]) if row["category"] in CATEGORIES else 0); dt=st.date_input("Date",value=date.fromisoformat(row["expense_date"])); notes=st.text_area("Notes",row["notes"]); save=st.form_submit_button("Save changes",type="primary")
                if save:
                    try: update_expense(selected,title,amount,cat,dt.isoformat(),notes); st.success("Transaction updated."); st.rerun()
                    except ValueError as e: st.error(str(e))
            with st.expander("Delete transaction",expanded=False):
                with st.form("delete_expense_form"):
                    confirm=st.checkbox(f"I understand this permanently deletes transaction #{selected}.",key="txn_delete_confirm"); delete=st.form_submit_button("Delete transaction")
                if delete:
                    if confirm: delete_expense(selected); st.success("Transaction deleted."); st.rerun()
                    else: st.error("Check the confirmation box before deleting.")

# ANALYTICS
elif page=="Analytics":
    header("Spending analytics","Explore the patterns behind your spending.","ANALYSIS")
    if df.empty: st.info("Add transactions to unlock your analytics.")
    else:
        c1,c2=st.columns([1,2]); start,end=range_filter(df,"analytics_dates"); cats=sorted(df.category.unique()); selected=c2.multiselect("Categories",cats,default=cats,key="analytics_cats")
        filtered=df[(df.category.isin(selected))&(df.expense_date.dt.date>=start)&(df.expense_date.dt.date<=end)]
        if filtered.empty: st.info("No transactions match the selected filters.")
        else:
            total=float(filtered.amount.sum()); average=float(filtered.amount.mean()); col1,col2,col3=st.columns(3); col1.metric("Filtered total",money(total)); col2.metric("Transactions",len(filtered)); col3.metric("Average transaction",money(average))
            l,r=st.columns(2,gap="large")
            with l: st.subheader("Category spending"); category_chart(filtered)
            with r:
                st.subheader("Daily spending"); daily=filtered.set_index("expense_date").resample("D").amount.sum().rename("Daily total (₹)"); st.line_chart(daily,height=300,color="#818cf8")
            st.subheader("Monthly spending"); monthly=monthly_totals(filtered.to_dict("records")); st.bar_chart(monthly.rename("Monthly total (₹)"),color="#818cf8")
            if len(monthly)>1:
                delta=monthly.iloc[-1]-monthly.iloc[-2]; st.caption(f"Latest month vs prior month: {'+' if delta>0 else '−'}{money(abs(delta))}.")
            with st.expander("View filtered transactions"): show_table(filtered)

# BUDGET
elif page=="Budget Planner":
    header("Budget planner","Set a monthly spending target and keep it in view.","MONTHLY PLAN")
    cols=st.columns(3); cols[0].metric("Monthly budget",money(budget) if budget else "Not set"); cols[1].metric("Spent this month",money(month_spend)); cols[2].metric("Remaining",money(max(0,budget-month_spend)) if budget else "—")
    if budget:
        ratio=month_spend/budget; st.progress(min(ratio,1.0),text=f"{ratio:.0%} of monthly budget used")
        if ratio>=1: st.error(budget_status())
        elif ratio>=.8: st.warning(budget_status())
        else: st.success(budget_status())
    with st.form("budget_form"):
        new_budget=st.number_input("Monthly budget (₹)",min_value=0.0,value=float(budget),step=500.0); save=st.form_submit_button("Save monthly budget",type="primary")
    if save:
        try: set_monthly_budget(new_budget); st.success("Monthly budget saved."); st.rerun()
        except ValueError as e: st.error(str(e))
    st.subheader("Category spending this month")
    if month_df.empty: st.caption("No category spending recorded for this month.")
    else:
        cats=month_df.groupby("category").amount.sum().sort_values(ascending=False)
        for cat,value in cats.items():
            c1,c2,c3=st.columns([2,4,1]); c1.write(cat); c2.progress(min(value/max(month_spend,1),1),text=f"{value/month_spend:.0%} of this month's spend"); c3.write(money(value))

# RULE-BASED INSIGHTS
elif page=="AI Spending Insights":
    header("Spending insights","Simple, transparent observations calculated from your records.","SMART INSIGHTS")
    st.caption("These are rule-based data summaries, not output from a large language model. ML forecasting is available separately.")
    if df.empty: st.info("Record a few expenses to reveal category and monthly patterns.")
    else:
        category_totals=df.groupby("category").amount.sum().sort_values(ascending=False); high=category_totals.index[0]
        c1,c2,c3=st.columns(3); c1.metric("Highest-spending category",high,money(category_totals.iloc[0])); c2.metric("Average transaction",money(df.amount.mean())); c3.metric("Current budget status","Not set" if not budget else f"{month_spend/budget:.0%} used")
        st.subheader("What stands out")
        st.markdown(f"- **{high}** is your highest-spending category across recorded transactions ({money(category_totals.iloc[0])}).")
        monthly=monthly_totals(expenses)
        if len(monthly)>1:
            change=monthly.iloc[-1]-monthly.iloc[-2]; pct=(change/monthly.iloc[-2]*100) if monthly.iloc[-2] else None
            wording=f"{abs(pct):.1f}%" if pct is not None else money(abs(change))
            st.markdown(f"- Spending changed by **{money(abs(change))}** ({wording}) compared with the preceding calendar month.")
        if budget:
            ratio=month_spend/budget
            if ratio>=1: st.error(budget_status())
            elif ratio>=.8: st.warning(budget_status())
            else: st.success(budget_status())
        st.subheader("Possible savings opportunities")
        monthly_categories=month_df.groupby("category").amount.sum().sort_values(ascending=False) if not month_df.empty else pd.Series(dtype=float)
        if len(monthly_categories):
            top=monthly_categories.index[0]; st.info(f"Review discretionary purchases in **{top}** first. It accounts for {money(monthly_categories.iloc[0])} this month. Compare upcoming purchases against your budget before committing.")
        else: st.caption("No current-month category data available yet.")

# MACHINE LEARNING
elif page=="ML Expense Prediction":
    header("Next-month forecast","A cautious estimate built from your recorded monthly spending.","MACHINE LEARNING")
    result=predict_next_month(expenses)
    if not result.ready: st.info(result.message)
    else:
        c1,c2=st.columns(2); c1.metric(f"Forecast · {result.next_month.strftime('%B %Y')}",money(result.prediction)); c2.metric("Model","Linear Regression")
        history=result.history.rename("Recorded monthly spending (₹)").to_frame(); history["Next-month forecast (₹)"]=float("nan"); history.loc[result.next_month,"Next-month forecast (₹)"]=result.prediction
        st.subheader("History and forecast"); st.line_chart(history,height=350,color=["#818cf8","#34d399"])
        if result.mae is not None: st.metric("Chronological holdout MAE",money(result.mae),help="Later observed months held out from fitting; this is a past error measure, not a guarantee.")
        else: st.caption("Evaluation is hidden because there are not enough monthly observations for a useful chronological holdout.")
        st.markdown('<div class="ss-section"><div class="ss-kicker">HOW TO READ THIS</div><p style="color:#aab6cb">The model fits a straight-line trend to your recorded monthly totals and extends it by one month. Empty calendar months between your first and last recorded transactions count as ₹0. No historical transactions are fabricated. A change in habits or a one-time expense can make the estimate inaccurate.</p></div>',unsafe_allow_html=True)

# DAA LAB
elif page=="DAA Lab":
    header("DAA lab","Explore sorting, searching and measured runtime side by side.","ALGORITHM WORKBENCH")
    tab1,tab2=st.tabs(["Algorithm demo","Performance lab"])
    with tab1:
        if df.empty: sample=[{"title":f"Example {i+1}","amount":v} for i,v in enumerate([450,120,450,80,920,210])]; st.caption("Illustrative inputs are used only in the algorithm demo until you have recorded transactions.")
        else: sample=df.head(16).to_dict("records")
        order=st.radio("Sort order",["Ascending","Descending"],horizontal=True,key="daa_order"); desc=order=="Descending"; amounts=[x["amount"] for x in sample]
        c1,c2=st.columns(2); c1.markdown("#### Merge Sort"); c1.code([x["amount"] for x in merge_sort(sample,desc)]); c2.markdown("#### Bubble Sort"); c2.code([x["amount"] for x in bubble_sort(sample,desc)])
        query=st.number_input("Binary Search · exact amount (₹)",min_value=0.0,value=float(amounts[0]) if amounts else 0.0,step=50.0,key="daa_search")
        matches=binary_search_amount(merge_sort(sample),query); st.success(f"Found {len(matches)} matching transaction(s).") if matches else st.info("No exact match in this dataset.")
        st.markdown("**Binary Search requires ascending sorted input.** It takes O(log n) to find a match; returning all k duplicate matches adds O(k).")
        with st.expander("Complexity reference"):
            st.dataframe(pd.DataFrame([{ "Algorithm":"Merge Sort","Best":"O(n log n)","Average":"O(n log n)","Worst":"O(n log n)","Space":"O(n)"},{"Algorithm":"Bubble Sort","Best":"O(n) with early exit","Average":"O(n²)","Worst":"O(n²)","Space":"O(1)"},{"Algorithm":"Binary Search","Best":"O(1)","Average":"O(log n)","Worst":"O(log n)","Space":"O(1) iterative"}]),hide_index=True,use_container_width=True)
    with tab2:
        st.write("Compare identical input values using independent copies. Synthetic data never touches your records.")
        source=st.radio("Benchmark dataset",["Recorded expenses","Synthetic dataset"],horizontal=True,key="bench_source")
        if source=="Recorded expenses": values=[float(x["amount"]) for x in expenses]; st.caption(f"{len(values)} recorded amounts")
        else: size=st.slider("Synthetic input size",100,5000,1000,100,key="bench_size"); values=synthetic_amounts(size); st.caption("Deterministic seeded values. They are not saved to SQLite.")
        repeats=st.select_slider("Timing repetitions",options=[1,3,5],value=3,key="bench_repeats")
        if st.button("Run benchmark",type="primary",key="bench_run"):
            with st.spinner("Measuring both algorithms…"): st.session_state.benchmark_result=benchmark_sorts(values,repeats)
        result=st.session_state.get("benchmark_result")
        if result:
            st.dataframe(pd.DataFrame([{ "Algorithm":"Bubble Sort","Input size":result["input_size"],"Median seconds":result["bubble_seconds"],"Best / average / worst":"O(n) / O(n²) / O(n²)","Extra space":"O(1)"},{"Algorithm":"Merge Sort","Input size":result["input_size"],"Median seconds":result["merge_seconds"],"Best / average / worst":"O(n log n) / O(n log n) / O(n log n)","Extra space":"O(n)"}]),hide_index=True,use_container_width=True)
            st.bar_chart(pd.Series({"Bubble Sort":result["bubble_seconds"],"Merge Sort":result["merge_seconds"]},name="Seconds"),color="#818cf8")
            st.caption("Small datasets and machine load can affect measured timings. Complexity describes scaling as input size grows.")

# ABOUT
elif page=="About Project":
    header("Designed for clarity","A B.Tech CSE PBL project that connects practical finance to core DAA concepts.","ABOUT PAISAWISE")
    st.markdown('<div class="ss-section"><h3>What it does</h3><p style="color:#aab6cb">Paisewise stores expense records locally, summarizes spending, tracks a monthly budget, demonstrates classical sorting and searching, compares measured execution time, and forecasts a future monthly total using scikit-learn.</p></div>',unsafe_allow_html=True)
    c1,c2=st.columns(2); c1.markdown("### Technology stack\nPython · Streamlit · SQLite · Pandas · Matplotlib · scikit-learn")
    c2.markdown("### Data handling\nThe default database is `expenses.db` beside `app.py`. `EXPENSE_TRACKER_DB` can point to another local database. Existing records persist across restarts.")
    st.markdown("### DAA concepts\nMerge Sort: O(n log n) time and O(n) extra space. Bubble Sort: O(n) best case with early termination, O(n²) average and worst. Binary Search: O(log n) on sorted data. Benchmark timings can vary with input size and system load.")
    st.markdown("### Forecast limits\nMonthly totals come from real dated expenses. Empty months between observed activity are set to zero. The linear model needs at least six months, and a holdout MAE is only shown when enough observations are available.")
    st.caption("For setup, tests, the full complexity table, and viva preparation, see README.md.")
