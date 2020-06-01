import os
a=os.popen('ls | grep Emb').readlines()
graphstats=open('graphstatsAll','w')
graphstats.write("div,func,subs,line,t,N,avgconn,nodeconn,clust,assort,shortpathl,networkcrit,netcritnorm,effegraphres")
appstats=open('appStatsAll','w')
appstats.write("div,funcs,subs,line,app,totalprocesstime,shortestprocess,longestrecv,process,output,recv")
for l in a:
    div=l.lstrip('EmbOut').split('-')[0].rstrip(' ').lstrip(' ')
    func=l.lstrip('EmbOut').split('-')[1].rstrip(' ').lstrip(' ')
    subs=l.lstrip('EmbOut').split('-')[2].rstrip(' ').lstrip(' ')
    t=open('%s/graphstats' % l.rstrip('\n'),'r')
    graphstats.write('\n')

    for line in t.readlines():
        if line[0]!='t':
            graphstats.write("%s,%s,%s,%s" % (div,func,subs,line))
    t.close()
    t=open('%s/appstats' % l.rstrip('\n'),'r')
    appstats.write('\n')

    for line in t.readlines():
        if line[0]!='a':
            appstats.write("%s,%s,%s,%s" % (div,func,subs,line))
appstats.close()
t.close()
graphstats.close()
