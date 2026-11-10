folder='E:\\projects\\\u5185\u5bb9\u521b\u4f5c\\\u6545\u4e8b\u77ed\u7247\\\u767d\u7c73\u996d\\\u540e\u671f\\\u5bfc\u6f14\u540e\u671f\u4fee\u6b63-v001\\\u5bfc\u51fa'
assert project.GetCurrentTimeline().GetName()=='v001_Director_Post_Repair_Final'
assert not project.IsRenderingInProgress()
project.SetCurrentRenderFormatAndCodec('mp4','H264_NVIDIA')
ok=project.SetRenderSettings({'SelectAllFrames':False,'MarkIn':0,'MarkOut':11055,'TargetDir':folder,'CustomName':'\u767d\u7c73\u996d-\u5bfc\u6f14\u4fee\u8ba2-v001-r3','ExportVideo':True,'ExportAudio':True,'FormatWidth':1344,'FormatHeight':768,'FrameRate':24,'AudioCodec':'aac','AudioSampleRate':48000})
assert ok
j=project.AddRenderJob();result={'job':j,'started':project.StartRendering([j])}
