import asyncio
import time
import statistics
from typing import List, Optional, Tuple

from renegade.client import AssembleExternalMatchOptions
from renegade.types import OrderSide, ExternalOrder, SignedExternalQuote, AtomicMatchApiBundle
from examples.helpers import (
    BASE_MINT, QUOTE_MINT, get_client
)

N_RUNS = 70  # Number of concurrent requests to run
HISTOGRAM_BINS = 5 # Number of bins for the text histogram
DELAY_MS = 500      # Delay between starting each request in milliseconds

async def request_and_assemble_timed(run_id: int) -> Optional[Tuple[float, AtomicMatchApiBundle]]:
    """Requests a quote, assembles it, and measures the round-trip time."""
    start_time = time.perf_counter()

    # Create the order (same order for all requests for simplicity)
    order = ExternalOrder(
        base_mint=BASE_MINT,
        quote_mint=QUOTE_MINT,
        side=OrderSide.SELL,
        quote_amount=10_000_000,  # $10 USDC
        min_fill_size=1_000_000,  # $1 USDC minimum
    )

    client = get_client()
    try:
        # Fetch quote
        print(f"Run {run_id}: Fetching quote...")
        quote: Optional[SignedExternalQuote] = await client.request_quote(order)
        if not quote:
            print(f"Run {run_id}: No quote found.")
            return None

        # Assemble quote
        print(f"Run {run_id}: Assembling quote...")
        options = AssembleExternalMatchOptions().with_allow_shared(True)
        bundle: Optional[AtomicMatchApiBundle] = await client.assemble_quote_with_options(quote, options)
        if not bundle:
            print(f"Run {run_id}: No bundle found.")
            return None

        end_time = time.perf_counter()
        round_trip_time = end_time - start_time
        print(f"Run {run_id}: Success (Time: {round_trip_time:.4f}s)")
        return round_trip_time

    except Exception as e:
        print(f"Run {run_id}: Error - {e}")
        return None

def print_histogram(times: List[float], num_bins: int) -> None:
    """Prints a simple text-based histogram."""
    if not times:
        print("No successful runs to generate histogram.")
        return

    min_time, max_time = min(times), max(times)
    if max_time == min_time:
        print(f"All {len(times)} runs took {min_time:.4f}s")
        return

    bin_size = (max_time - min_time) / num_bins
    bins = [0] * num_bins

    for t in times:
        bin_index = min(int((t - min_time) / bin_size), num_bins - 1)
        # Handle edge case where t == max_time
        if t == max_time:
            bin_index = num_bins - 1
        bins[bin_index] += 1

    print("\nRound-trip Time Histogram:")
    max_bin_count = max(bins) if bins else 0
    scale = 50 / max_bin_count if max_bin_count > 0 else 1

    for i in range(num_bins):
        bin_start = min_time + i * bin_size
        bin_end = bin_start + bin_size
        bar = '#' * int(bins[i] * scale)
        print(f"[{bin_start:.4f}s - {bin_end:.4f}s) | {bar} ({bins[i]})")


async def main() -> None:
    """Runs N_RUNS concurrent quote requests and prints timing statistics."""
    print(f"Starting {N_RUNS} concurrent quote/assemble requests with {DELAY_MS}ms delay between starts...")

    tasks = []
    for i in range(N_RUNS):
        print(f"Starting task {i}...")
        task = asyncio.create_task(request_and_assemble_timed(i))
        tasks.append(task)
        if i < N_RUNS - 1: # Don't sleep after the last task
            await asyncio.sleep(DELAY_MS / 1000.0)

    print("\nWaiting for all tasks to complete...")
    results = await asyncio.gather(*tasks)

    successful_times: List[float] = []
    successful_bundles: List[AtomicMatchApiBundle] = []
    for result in results:
        if result:
            time_taken = result
            successful_times.append(time_taken)

    print(f"\n--- Results ---")
    print(f"Successful runs: {len(successful_times)} / {N_RUNS}")

    if successful_times:
        min_time = min(successful_times)
        max_time = max(successful_times)
        mean_time = statistics.mean(successful_times)
        median_time = statistics.median(successful_times)
        stdev_time = statistics.stdev(successful_times) if len(successful_times) > 1 else 0.0

        print("\nTiming Statistics (seconds):")
        print(f"  Min:    {min_time:.4f}")
        print(f"  Max:    {max_time:.4f}")
        print(f"  Mean:   {mean_time:.4f}")
        print(f"  Median: {median_time:.4f}")
        print(f"  StdDev: {stdev_time:.4f}")

        print_histogram(successful_times, HISTOGRAM_BINS)
    else:
        print("\nNo successful runs to calculate statistics.")


if __name__ == "__main__":
    # Need to import execute_bundle_async if used
    # from examples.helpers import execute_bundle_async
    asyncio.run(main()) 