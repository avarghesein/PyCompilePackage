import os

def Main():
    print('Hello from DemoStandalone App')

    import ASubNamespace.Feature1 as F1

    print (F1.MyFeature())

    import ASubNamespace.AnotherSubNameSpace.Feature2 as F2

    print (F2.MyFeature2())
    

if __name__ == "__main__":
    Main()