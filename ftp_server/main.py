import watchdog_classes
from concurrent.futures import ProcessPoolExecutor

if __name__ == '__main__':
    watch = watchdog_classes.OnMyWatch()
    with ProcessPoolExecutor(max_workers=3) as executor:
        executor.submit(watch.run())