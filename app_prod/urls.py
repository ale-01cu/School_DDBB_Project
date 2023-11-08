from django.urls import path, re_path
from .views.ProductosViews import (
    crearProducto, 
    obtenerUnProducto, 
    eliminarProducto, 
    actualizarProducto, 
    getProductos,
    search_products,
    filter_products,
    get_productos_vacios,
)
from .views.ProveedorViews import listProveedor, crearProveedor, eliminarProveedor
from .views.PedidosViews import get_pedidos, addPedido
from .views.CarritoViews import addCarrito, getCarrito, eliminarDelCarrito
from .views.ConfirmacionesViews import crearConfirmacion
from .views.InformeVentaViews import listInfoVentas
from .views.opcionesExtras import (
  opcionesExtras, 
  poblarProductos, 
  poblarClientes, 
  poblarEmpleados,
  poblarProveedores,
  poblarPedidos
)
from .views.historialView import get_historial
from .views.opcionesExtras import aumentar_precios, disminuir_precios

urlpatterns = [
  path('home/', getProductos, name='home'),
  path('crear/', crearProducto, name='postProductos'),
  path('obtener/<int:pk>/', obtenerUnProducto, name='obtenerProducto'),
  path('eliminar/<int:pk>/', eliminarProducto, name='eliminarProducto'),
  path('actualizar/<int:pk>/', actualizarProducto, name='actualizarProducto'),
  path('home/search/', search_products, name='searchProduct'),
  path('home/filter/', filter_products, name='filterProduct'),
  path('vacios/', get_productos_vacios, name='emptyProducts'),
  path('historial/', get_historial, name='history'),
  
  path('proveedores/', listProveedor, name='listProveedor'),
  path('proveedores/crear/', crearProveedor, name='crearProveedor'),
  path('proveedores/eliminar/<int:pk>/', eliminarProveedor, name='eliminarProveedor'),
  
  path('pedidos/', get_pedidos, name='pedidos'),
  path('pedidos/add/<int:id_prod>', addPedido, name='addPedidos'),
  
  path('carrito/', getCarrito, name='verCarrito'),
  path('carrito/add/<int:id_prod>', addCarrito, name='addCarrito'),
  path('carrito/eliminar/<int:id_prod>', eliminarDelCarrito, name='eliminarDelCarrito'),
  
  path('confirmacion/<int:id_pedido>', crearConfirmacion, name='confirmar'),
  # path('confirmacion/eliminar/<int:id_pedido>', quitarConfirmacion, name='eliminarConfirmacion'),
  
  path('ventas/', listInfoVentas, name='ventas'),
  
  path('extras/', opcionesExtras, name='extras'),
  path('extras/aumentar-precio/', aumentar_precios, name='aumentar-precio'),
  path('extras/disminuir-precio/', disminuir_precios, name='disminuir-precio'),
  path('poblar-productos/', poblarProductos, name='poblar-productos'),
  path('poblar-clientes/', poblarClientes, name='poblar-clientes'),
  path('poblar-empleados/', poblarEmpleados, name='poblar-empleados'),
  path('poblar-proveedores/', poblarProveedores, name='poblar-proveedores'),
  path('poblar-pedidos/', poblarPedidos, name='poblar-pedidos')
  
]