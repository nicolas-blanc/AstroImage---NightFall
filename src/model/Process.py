

class Process(object):
    """docstring for Process"""
    def __init__(self, origin):
        super(Process, self).__init__()
        if type(origin) == image:
            self.m_origin = origin
        elif type(origin) == list:
            pass #Traitement a effectue en dans le cas d'une liste d'image
        else:
            raise AttributeError, "Ce type n'est pas traité dans la classe Process"+str(type(data))
        self.m_result = null


    # proceed() : void
    def proceed(self):
        pass


    # setData(picture : Image) : void
    # setData(pictures : List<Image>) : void
    def setData(self, picture):
        if type(origin) == image:
            self.m_origin = origin
        elif type(origin) == list:
            pass #Traitement a effectue en dans le cas d'une liste d'image
        else:
            raise AttributeError, "Ce type n'est pas traité dans la classe Process"+str(type(data))


    # getResult() : Image
    def getResult(self):
        return m_result


class ProcessPreTreatment(Process):
    """docstring for ProcessPreTreatment"""
    def __init__(self, origin):
        super(ProcessPreTreatment, self).__init__(origin)

    
