setTimeout(() => {
    document.querySelectorAll('.flash-stack .alert')
        .forEach(el => bootstrap.Alert.getOrCreateInstance(el).close());
}, 5000);