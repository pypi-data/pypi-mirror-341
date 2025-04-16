import logging
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

# --- Import django-scopes ---
from django_scopes import scope

# --- Use Pretix Celery app instance ---
from pretix.celery_app import app
# --- Import necessary Pretix models ---
from pretix.base.models import Order, Organizer  # Import Organizer

# --- Import your Geocode model and geocoding functions ---
from .models import OrderGeocodeData
from .geocoding import (
    get_formatted_address_from_order,
    geocode_address,
    DEFAULT_NOMINATIM_USER_AGENT
)

logger = logging.getLogger(__name__)


@app.task(bind=True, max_retries=3, default_retry_delay=60, ignore_result=True)
def geocode_order_task(self, order_pk: int, nominatim_user_agent: str | None = None):
    """
    Celery task to geocode the address for a given order PK.
    Accepts the Nominatim User-Agent as an argument.
    Activates django-scopes organizer scope before querying scoped models.
    """
    order = None  # Initialize order to None
    try:
        try:
            order = Order.objects.select_related('event__organizer', 'invoice_address').get(pk=order_pk)
            organizer = order.event.organizer  # Get organizer from the fetched order
        except ObjectDoesNotExist:
            logger.error(f"Order with PK {order_pk} not found in geocode_order_task.")
            return
        with scope(organizer=organizer):
            logger.info(
                f"Starting geocoding task for Order {order.code} (PK: {order_pk}) within scope of Organizer '{organizer.slug}'")

            relation_name = 'geocode_data'  # Ensure this matches your model
            # Check existence within scope (safer)
            if OrderGeocodeData.objects.filter(order_id=order_pk).exists():
                logger.info(f"Geocode data already exists for Order {order.code} (checked within scope). Skipping.")
                return

            address_str = get_formatted_address_from_order(order)
            if not address_str:
                logger.info(f"Order {order.code} has no address suitable for geocoding. Storing null coordinates.")
                # Store null within scope
                with transaction.atomic():
                    OrderGeocodeData.objects.update_or_create(
                        order=order, defaults={'latitude': None, 'longitude': None}
                    )
                return

            logger.debug(f"Attempting to geocode address for Order {order.code}: '{address_str}'")
            coordinates = geocode_address(address_str, nominatim_user_agent=nominatim_user_agent)

            # Store result within scope
            with transaction.atomic():
                if coordinates:
                    latitude, longitude = coordinates
                    obj, created = OrderGeocodeData.objects.update_or_create(
                        order=order, defaults={'latitude': latitude, 'longitude': longitude}
                    )
                    log_level = logging.INFO if created else logging.DEBUG
                    logger.log(log_level,
                               f"Saved{' new' if created else ' updated'} geocode data for Order {order.code}: ({latitude}, {longitude})")
                else:
                    logger.warning(f"Geocoding failed for Order {order.code}. Storing null coordinates.")
                    obj, created = OrderGeocodeData.objects.update_or_create(
                        order=order, defaults={'latitude': None, 'longitude': None}
                    )
                    log_level = logging.INFO if created else logging.DEBUG
                    logger.log(log_level,
                               f"Saved{' new' if created else ' updated'} null geocode data for Order {order.code} after failed attempt.")
        # --- Scope deactivated automatically here ---

    # Keep outer exception handling
    except ObjectDoesNotExist:
        # This case is now handled earlier, but keep for safety
        logger.error(f"Order with PK {order_pk} not found outside scope handling.")
    except Exception as e:
        logger.exception(
            f"Unexpected error in geocode_order_task for Order PK {order_pk} (potentially outside scope): {e}")
        # Retry on unexpected errors before scope activation
        raise self.retry(exc=e)
