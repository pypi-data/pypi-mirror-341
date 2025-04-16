# Alert Block

Using the `md alert` tag in a multiline block will render an alert message looking like this : 

```md alert
# This is an alert message
```

Note that the content of the block must start with a `#` character, which will be used as the title of the alert. The rest of the content will be used as the body of the alert.

```md alert
# This is an alert message
This is the body of the alert message.
```

## Level of alert
The level of the alert can be set using the `level` attribute. The default level is `info`, but you can set it to `success`, `warning`, or `error` as well.

```md alert success
# This is a success alert message
```

```md alert warning
# This is a warning alert message
```

```md alert error
# This is an error alert message
```


