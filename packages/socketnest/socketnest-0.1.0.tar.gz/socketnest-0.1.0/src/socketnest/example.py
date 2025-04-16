from socketnest import Socketnest

socketnest = Socketnest(
    app_id="9508896", secret="TllSnaPtCAF2PnYHysdlrQ"
)

res = socketnest.trigger(
    channel="test", event="test", data={"message": "Hello, SocketNest!"})

print(res.json())
