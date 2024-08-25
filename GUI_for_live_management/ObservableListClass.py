class ObservableList(list):
    def __init__(self, *args, **kwargs):
        super(ObservableList, self).__init__(*args, **kwargs)
        self.callbacks = []

    def register_callback(self, callback):
        self.callbacks.append(callback)

    def notify(self, item):
        for callback in self.callbacks:
            callback(item)

    def append(self, item):
        super(ObservableList, self).append(item)
        self.notify(item)

    def remove(self, item):
        super(ObservableList, self).remove(item)
        self.notify(item)

    def extend(self, iterable):
        super(ObservableList, self).extend(iterable)
        self.notify(iterable)

    def pop(self, index=-1):
        item = super(ObservableList, self).pop(index)
        #self.notify()
        return item

    def __setitem__(self, index, item):
        super(ObservableList, self).__setitem__(index, item)
        #self.notify()

    def __delitem__(self, index):
        super(ObservableList, self).__delitem__(index)
        #self.notify()

# Usage
def list_changed(lst):
    print(f"List changed: {lst}")

# ol = ObservableList()
# ol.register_callback(list_changed)
# ol.append(1)  # This will trigger the callback
# ol.remove(1)  # This will also trigger the callback
