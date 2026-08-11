from sqlalchemy import select

from app.db.session import SessionLocal as ShopSessionLocal
from app.models.image import Image

from photo_service.models.photo import Photo
from photo_service.repositories.photo_repository import PhotoRepository
from photo_service.sharding.router import (
    get_session_factory,
    get_shard_number,
)


def main() -> None:
    migrated = 0
    skipped = 0

    with ShopSessionLocal() as shop_db:
        images = list(
            shop_db.scalars(
                select(Image)
            ).all()
        )

        print(f"Found {len(images)} legacy image(s)")

        for image in images:
            shard = get_shard_number(image.id)
            session_factory = get_session_factory(image.id)

            with session_factory() as shard_db:
                repository = PhotoRepository(shard_db)

                existing = repository.get_by_id(image.id)

                if existing is not None:
                    if existing.image != image.image:
                        raise RuntimeError(
                            f"Photo {image.id} already exists "
                            "but binary content differs"
                        )

                    print(
                        f"SKIP {image.id} -> shard {int(shard)} "
                        "(already migrated)"
                    )
                    skipped += 1
                    continue

                try:
                    photo = Photo(
                        id=image.id,
                        image=image.image,
                    )

                    repository.create(photo)
                    shard_db.commit()

                except Exception:
                    shard_db.rollback()
                    raise

                print(
                    f"MIGRATED {image.id} -> shard {int(shard)}"
                )
                migrated += 1

    print(
        f"Done. migrated={migrated}, skipped={skipped}"
    )


if __name__ == "__main__":
    main()
