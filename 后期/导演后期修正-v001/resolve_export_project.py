base='E:\\projects\\\u5185\u5bb9\u521b\u4f5c\\\u6545\u4e8b\u77ed\u7247\\\u767d\u7c73\u996d\\\u540e\u671f\\\u5bfc\u6f14\u540e\u671f\u4fee\u6b63-v001'
tl=project.GetCurrentTimeline()
assert tl.GetName()=='v001_Director_Post_Repair_Final' and not project.IsRenderingInProgress()
for n in ['B21_GB016-1_02','B42_GB031_02']:
 c=next(c for c in tl.GetItemListInTrack('video',1) if c.GetName()==n)
 assert c.ExportFusionComp(base+'/'+n+'.comp',1)
result={'save':resolve.GetProjectManager().SaveProject(),'drp':resolve.GetProjectManager().ExportProject(project.GetName(),base+'/\u767d\u7c73\u996d-\u5bfc\u6f14\u4fee\u8ba2-v001.drp',True),'drt':tl.Export(base+'/\u5bfc\u6f14\u4fee\u8ba2-v001.drt',resolve.EXPORT_DRT,resolve.EXPORT_NONE)}
resolve.OpenPage('edit');tl.SetCurrentTimecode('00:06:26:03')
