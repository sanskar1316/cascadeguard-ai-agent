import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
st.set_page_config(page_title='CascadeGuard AI', page_icon='🛡️', layout='wide')
st.title('🛡️ CascadeGuard AI')
st.subheader('Single Intelligent Agent for Failure Prevention')
st.write('This simulator analyzes a dependency network, estimates how a component failure may spread, and recommends a preventive action.')
st.warning('Educational prototype only: simulated data and a simple decision rule; it does not monitor or repair real servers.')
with st.sidebar:
    st.header('Network setup')
    nodes_text=st.text_area('Components (one per line)','Web App\nAPI Service\nAuth Service\nDatabase\nUser Login\nReports\nPayments\nOrder Service\nNotifications',height=180)
    edges_text=st.text_area('Dependencies (source -> target, one per line)','Web App -> API Service\nAPI Service -> Auth Service\nAPI Service -> Database\nAuth Service -> User Login\nDatabase -> Reports\nDatabase -> Payments\nPayments -> Order Service\nOrder Service -> Notifications',height=200)
    nodes=[x.strip() for x in nodes_text.splitlines() if x.strip()]
    selected=st.selectbox('Simulate failure in',nodes or ['Web App'])
    st.button('Analyze network',type='primary')
def make_graph(nodes_text,edges_text):
    graph=nx.DiGraph()
    graph.add_nodes_from([x.strip() for x in nodes_text.splitlines() if x.strip()])
    errors=[]
    for i,line in enumerate(edges_text.splitlines(),1):
        line=line.strip()
        if not line: continue
        if '->' not in line:
            errors.append(f'Line {i}: use source -> target'); continue
        a,b=[x.strip() for x in line.split('->',1)]
        if not a or not b:
            errors.append(f'Line {i}: both component names are required'); continue
        graph.add_edge(a,b)
    return graph,errors
def downstream(graph,start):
    found,queue=set(),deque([start])
    while queue:
        current=queue.popleft()
        for nxt in graph.successors(current):
            if nxt not in found and nxt!=start:
                found.add(nxt); queue.append(nxt)
    return found
G,errors=make_graph(nodes_text,edges_text)
for error in errors: st.error(error)
if not G.nodes:
    st.info('Add at least one component in the sidebar.'); st.stop()
if selected not in G:
    st.error('Selected component is not part of the network.'); st.stop()
affected=downstream(G,selected)
left,right=st.columns([1.2,1])
with left:
    st.subheader('Dependency network')
    fig,ax=plt.subplots(figsize=(9,5)); pos=nx.spring_layout(G,seed=8)
    colors=['#e85d5d' if n==selected else '#ffbd69' if n in affected else '#62b6cb' for n in G.nodes]
    nx.draw_networkx(G,pos,ax=ax,node_color=colors,node_size=1900,font_size=8,arrows=True,arrowsize=18,edge_color='#718096')
    ax.set_axis_off(); st.pyplot(fig,use_container_width=True)
    st.caption('Red = selected failure | Orange = potentially affected | Blue = other components')
with right:
    st.subheader("Agent's analysis")
    st.metric('Components',len(G.nodes)); st.metric('Potentially affected components',len(affected))
    st.write('**Potential downstream impact:** '+(', '.join(sorted(affected)) if affected else 'None connected downstream.'))
    candidates=[
      {'name':f'Protect or add redundancy to {selected}','benefit':len(affected),'risk':1,'reason':'Direct protection can reduce the chance that the selected component becomes unavailable.'},
      {'name':'Prepare an alternate route for dependent services','benefit':max(1,len(affected)-1),'risk':2,'reason':'An alternate route may keep dependent services running if a valid backup path exists.'}]
    for c in candidates: c['score']=2*c['benefit']-c['risk']
    candidates.sort(key=lambda c:c['score'],reverse=True)
    st.write('**Candidate actions**')
    for i,c in enumerate(candidates,1): st.markdown(f"{i}. **{c['name']}** — score {c['score']} (risk {c['risk']})")
    best=candidates[0]; st.success('Recommended action: '+best['name']); st.write(best['reason'])
st.subheader('Single-agent decision cycle')
cols=st.columns(5)
for col,title,detail in zip(cols,['1. Observe','2. Analyze','3. Evaluate','4. Decide','5. Review'],['Read components and links.','Trace possible failure impact.','Score benefit and risk.','Select the best-scoring action.','Review the simulated result.']):
    col.markdown(f'**{title}**'); col.caption(detail)
with st.expander('How does the decision score work?'):
    st.latex(r'\text{Score} = 2 \times \text{Estimated Benefit} - \text{Risk}')
    st.write('This is a transparent demonstration heuristic, not a trained machine-learning model. A stronger version can add weighted links, failure probabilities, action costs, and before/after evaluation.')
with st.expander('Try it'):
    st.write('Choose a different failed component or edit dependency links in the sidebar. Try Database or API Service.')
