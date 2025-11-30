from sqlmodel import select
from .models import SerieDocumentos, Usuario, Entidad, Articulo, Cotizacion, CotizacionLinea
from .database import get_session

async def run_seed():
    # Usamos el generador get_session
    async for session in get_session():
        # Verificar si ya existen datos
        result = await session.exec(select(SerieDocumentos))
        if result.first():
            return # Ya hay datos, no hacemos nada

        print("Insertando datos de prueba...")
        
        s = SerieDocumentos(id=4, name="presupuesto", doc_mod_name="presupuestos", prefix="PR", current_number=100)
        u = Usuario(id=103, name="Luis Ku", username="luis", email="luis@example.com")
        e = Entidad(id=54, name="Ferretería", rfc="XAXX010101000", address="Centro")
        a = Articulo(id=221, code="PRD001", name="Laptop ABC", unit="pz", price=15000.0)
        c = Cotizacion(id=1, ser_fol="COT-001", ser_doc=4, alt_usr=103, ent_id=54, est=0)
        
        session.add(s)
        session.add(u)
        session.add(e)
        session.add(a)
        session.add(c)
        await session.commit()
        
        # Linea requiere cotizacion creada
        l = CotizacionLinea(id=1001, cot_id=1, art_id=221, cantidad=2, precio=15000.0, subtotal=30000.0)
        session.add(l)
        await session.commit()
        print("Datos insertados!")
        break